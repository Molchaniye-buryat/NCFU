import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
from scipy.special import lambertw

q = 1.602e-19
k = 1.381e-23
e0 = 8.854e-14

MAT = {
    'Si':  dict(Eg0=1.166,  alpha=4.730e-4, beta=636,
                 Nc300=2.8e19, Nv300=1.04e19, er=11.7, mun=1350, mup=480),
    'Ge':  dict(Eg0=0.7437, alpha=4.774e-4, beta=235,
                 Nc300=1.04e19, Nv300=6.0e18, er=16.2, mun=3900, mup=1900),
    'GaAs':dict(Eg0=1.519,  alpha=5.405e-4, beta=204,
                 Nc300=4.7e17, Nv300=7.0e18, er=12.9, mun=8500, mup=400),
}

mat   = MAT['Si']
Na, Nd = 1e17, 1e17
S      = 1e-2
Rs     = 1.0
n_id   = 1.0
tau    = 1e-6


def UT(T):
    return k * T / q

def Eg(T, m):
    return m['Eg0'] - m['alpha'] * T**2 / (T + m['beta'])

def ni(T, m):
    Nc = m['Nc300'] * (T / 300.0) ** 1.5
    Nv = m['Nv300'] * (T / 300.0) ** 1.5
    return np.sqrt(Nc * Nv) * np.exp(-Eg(T, m) / (2 * UT(T)))

def carriers(Na_, Nd_, T, m):
    n_i = ni(T, m)
    return Nd_, n_i**2 / Nd_, Na_, n_i**2 / Na_

def phi0(Na_, Nd_, T, m):
    return UT(T) * np.log(Na_ * Nd_ / ni(T, m)**2)

def W_depl(U, Na_, Nd_, T, m):
    es = m['er'] * e0
    return np.sqrt(2 * es * (phi0(Na_, Nd_, T, m) - U) / q * (Na_ + Nd_) / (Na_ * Nd_))

def Isat(Na_, Nd_, S_, T, m, tau_=tau):
    Dn, Dp = m['mun'] * UT(T), m['mup'] * UT(T)
    Ln, Lp = np.sqrt(Dn * tau_), np.sqrt(Dp * tau_)
    return q * S_ * ni(T, m)**2 * (Dp / (Lp * Nd_) + Dn / (Ln * Na_))


def diode_I(U, Is, Rs_, n_, T):
    vt = n_ * UT(T)
    f = lambda I: I - Is * (np.exp((U - I * Rs_) / vt) - 1.0)
    I_hi = max(1.0, Is * np.exp(60.0))
    try:
        return brentq(f, -Is * 1.001, I_hi, maxiter=200)
    except ValueError:
        return brentq(f, -Is * 1.001, 10.0, maxiter=200)

def diode_I_lambert(U, Is, Rs_, n_, T):
    vt = n_ * UT(T)
    if Rs_ == 0:
        return Is * (np.exp(U / vt) - 1.0)
    arg = (Is * Rs_ / vt) * np.exp((U + Is * Rs_) / vt)
    W = lambertw(arg).real
    return (vt / Rs_) * W - Is


# =========================================================================
#  1. Контрольные значения при 300 К (для самопроверки)
# =========================================================================
T0 = 300.0
n_i0 = ni(T0, mat)
nn, pn, pp, np_ = carriers(Na, Nd, T0, mat)
phi0_0 = phi0(Na, Nd, T0, mat)
W0 = W_depl(0.0, Na, Nd, T0, mat)
Is0 = Isat(Na, Nd, S, T0, mat)

print("=== Контрольные значения (300 К) ===")
print(f"ni(300K)      = {n_i0:.3e} см^-3   (ожид. (6..10)e9)")
print(f"nn = {nn:.3e}, pn = {pn:.3e} см^-3")
print(f"pp = {pp:.3e}, np = {np_:.3e} см^-3")
print(f"закон действия масс nn*pn = {nn*pn:.3e}  vs ni^2 = {n_i0**2:.3e}")
print(f"phi0(300K)    = {phi0_0:.4f} В        (ожид. ~0.82 В)")
print(f"W(0) при 300K = {W0*1e4:.4f} мкм      (ожид. ~0.1 мкм)")
print(f"Is(300K)      = {Is0:.3e} А          (ожид. ~1e-14 А)")


# =========================================================================
#  2. График ni(T) в диапазоне 200-500 К (лог. шкала)
# =========================================================================
T_range = np.linspace(200, 500, 300)
plt.figure(figsize=(7, 5))
for name in ['Si', 'Ge', 'GaAs']:
    ni_vals = [ni(T, MAT[name]) for T in T_range]
    plt.semilogy(T_range, ni_vals, label=name)
plt.xlabel('T, K')
plt.ylabel(r'$n_i$, см$^{-3}$')
plt.title('Собственная концентрация носителей $n_i(T)$')
plt.legend()
plt.grid(True, which='both', alpha=0.3)
plt.tight_layout()
plt.savefig(r"E:\NCFU\2 курс\Физические основы информационных технологий\лаба1\fig1_ni_T.png", dpi=150)
plt.close()


# =========================================================================
#  3. ВАХ диода при трёх температурах, без Rs (лин. и полулог. шкалы)
# =========================================================================
T_list = [275, 300, 325]
U_arr = np.linspace(0.0, 0.8, 400)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
for T in T_list:
    Is_T = Isat(Na, Nd, S, T, mat)
    I_arr = np.array([diode_I(U, Is_T, 0.0, n_id, T) for U in U_arr])
    axes[0].plot(U_arr, I_arr * 1e3, label=f'T={T} K')
    axes[1].semilogy(U_arr, np.abs(I_arr), label=f'T={T} K')

axes[0].set_xlabel('U, В'); axes[0].set_ylabel('I, мА')
axes[0].set_title('ВАХ (линейная шкала), Rs=0'); axes[0].legend(); axes[0].grid(alpha=0.3)

axes[1].set_xlabel('U, В'); axes[1].set_ylabel('I, А')
axes[1].set_title('ВАХ (полулог. шкала), Rs=0'); axes[1].legend(); axes[1].grid(alpha=0.3, which='both')
plt.tight_layout()
plt.savefig(r"E:\NCFU\2 курс\Физические основы информационных технологий\лаба1\fig2_IV_3temps.png", dpi=150)
plt.close()

# оценка наклона прямой ветви (мВ/декаду) при T=300K
Is_300 = Isat(Na, Nd, S, 300, mat)
U1, U2 = 0.5, 0.6
I1 = diode_I(U1, Is_300, 0.0, n_id, 300)
I2 = diode_I(U2, Is_300, 0.0, n_id, 300)
slope = (U2 - U1) / (np.log10(I2) - np.log10(I1))
print(f"\nНаклон прямой ветви при 300K: {slope*1000:.1f} мВ/декаду (ожид. ~60n мВ/дек)")


# =========================================================================
#  4. Влияние Rs: сравнение численного и аналитического (Ламберта) решений
# =========================================================================
Rs_list = [0, 1, 10, 100]
U_arr2 = np.linspace(0.0, 0.9, 300)

plt.figure(figsize=(7, 5))
for Rs_ in Rs_list:
    I_num = np.array([diode_I(U, Is_300, Rs_, n_id, 300) for U in U_arr2])
    plt.plot(U_arr2, I_num * 1e3, label=f'Rs={Rs_} Ом')
plt.xlabel('U, В'); plt.ylabel('I, мА')
plt.title('ВАХ при разных Rs (T=300K)')
plt.legend(); plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig(r"E:\NCFU\2 курс\Физические основы информационных технологий\лаба1\fig3_IV_Rs.png", dpi=150)
plt.close()

# сравнение численного и Ламберт-решения на одной кривой (Rs=1 Ом)
# сравниваем только на прямой ветви при заметном токе (>1 нА) — иначе относительная
# погрешность формально "взрывается" из-за деления на околонулевой обратный ток
mask = U_arr2 > 0.2
I_num  = np.array([diode_I(U, Is_300, 1.0, n_id, 300) for U in U_arr2[mask]])
I_lam  = np.array([diode_I_lambert(U, Is_300, 1.0, n_id, 300) for U in U_arr2[mask]])
rel_err = np.abs((I_num - I_lam) / np.abs(I_num))
print(f"Максимальная относительная погрешность brentq vs Lambert (Rs=1 Ом, U>0.2В): {rel_err.max():.2e}")


print("\nГотово: графики сохранены как fig1_ni_T.png, fig2_IV_3temps.png, fig3_IV_Rs.png")


# =========================================================================
#  5. ВАРИАНТ №4: GaAs, Na=Nd=1e17 см^-3, S=1e-3 см^2, Rs=5 Ом, n=1.0
#     (переопределяем параметры — дальше используем те же функции выше)
# =========================================================================
mat_v   = MAT['GaAs']
Na_v, Nd_v = 1e17, 1e17
S_v        = 1e-3
Rs_v       = 5.0
n_v        = 1.0

T0v = 300.0
ni_v = ni(T0v, mat_v)
nn_v, pn_v, pp_v, np_v = carriers(Na_v, Nd_v, T0v, mat_v)
phi0_v = phi0(Na_v, Nd_v, T0v, mat_v)
W0_v   = W_depl(0.0, Na_v, Nd_v, T0v, mat_v)
Is_v300 = Isat(Na_v, Nd_v, S_v, T0v, mat_v)

print("\n=== Вариант 4 (GaAs), 300 К ===")
print(f"ni      = {ni_v:.3e} см^-3")
print(f"nn={nn_v:.3e}, pn={pn_v:.3e}, pp={pp_v:.3e}, np={np_v:.3e} см^-3")
print(f"phi0    = {phi0_v:.4f} В")
print(f"W(0)    = {W0_v*1e4:.4f} мкм")
print(f"Is(300K)= {Is_v300:.3e} А")

# ---- Индивидуальное задание варианта 4: ВАХ при 300, 375, 450 К ----
T_var4 = [300, 375, 450]
U_arr4 = np.linspace(0.0, 1.4, 500)

def U_from_I(I, Is_, Rs_, n_, T):
    return n_ * UT(T) * np.log(I / Is_ + 1.0) + I * Rs_

plt.figure(figsize=(7.5, 5.5))
for T in T_var4:
    Is_T = Isat(Na_v, Nd_v, S_v, T, mat_v)
    I_arr = np.array([diode_I(U, Is_T, Rs_v, n_v, T) for U in U_arr4])
    plt.semilogy(U_arr4, np.clip(I_arr, 1e-30, None), label=f'T={T} K')

    I1v, I2v = 50 * Is_T, 500 * Is_T
    U1v = U_from_I(I1v, Is_T, Rs_v, n_v, T)
    U2v = U_from_I(I2v, Is_T, Rs_v, n_v, T)
    slope_v = (U2v - U1v) / (np.log10(I2v) - np.log10(I1v)) * 1000
    print(f"T={T} K: Is={Is_T:.3e} A, наклон = {slope_v:.1f} мВ/декаду "
          f"(теор. 60*n*T/300 = {60*n_v*T/300:.1f} мВ/дек)")

plt.xlabel('U, В'); plt.ylabel('I, А')
plt.ylim(1e-14, 1.0)
plt.title('Вариант 4: ВАХ GaAs-диода при трёх температурах (Rs=5 Ом)')
plt.legend(); plt.grid(alpha=0.3, which='both')
plt.tight_layout()
plt.savefig(r"E:\NCFU\2 курс\Физические основы информационных технологий\лаба1\fig4_variant4_GaAs.png", dpi=150)
plt.close()

print("\nГрафик индивидуального задания сохранён как fig4_variant4_GaAs.png")