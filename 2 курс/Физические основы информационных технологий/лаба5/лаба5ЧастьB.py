import numpy as np
import matplotlib.pyplot as plt

VARIANT = 4                 # номер варианта
V_ER0 = -3.0                # В, исходный порог стёртого состояния
V_PR0 = 2.0                 # В, исходный порог записанного состояния
A_E = 6.0e-3                # В, коэффициент деградации стирания
A_P = 1.8e-3                # В, коэффициент деградации записи
BETA_E = 0.70               # показатель степени для стирания
BETA_P = 0.70               # показатель степени для записи
SIG0 = 0.10                 # В, исходный СКО распределения Vth
N0 = 1e5                    # циклов, параметр роста разброса
GAMMA = 0.5                 # показатель роста разброса
K_G = 6.0                   # защитный коэффициент
W_MIN = 1.8                 # В, минимально допустимое окно
M_CELL = 1e9                # число ячеек в массиве
NOISE = 0.07                # относительный шум "эксперимента"

W0 = V_PR0 - V_ER0

def v_erase(N):
    return V_ER0 + A_E * np.power(N, BETA_E)

def v_prog(N):
    return V_PR0 + A_P * np.power(N, BETA_P)

def window(N):
    return v_prog(N) - v_erase(N)

def sigma(N):
    return SIG0 * (1.0 + np.power(N / N0, GAMMA))

def bits_per_cell(N):
    w = np.maximum(window(N), 0.0)
    return np.log2(1.0 + w / (K_G * sigma(N)))

def endurance_analytic(wmin=W_MIN):
    return ((W0 - wmin) / (A_E - A_P)) ** (1.0 / BETA_E)

def endurance_numeric(wmin=W_MIN):
    N = np.logspace(0, 8, 200000)
    i = np.argmax(window(N) < wmin)
    return N[i] if i > 0 else np.nan

def fit_power_law(N, dV):
    beta, logA = np.polyfit(np.log10(N), np.log10(dV), 1)
    return 10 ** logA, beta

N = np.logspace(0, 6, 1000)
Ne = endurance_analytic()

# Задание 1
fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.5))
ax[0].semilogx(N, v_erase(N), 'b', lw=2, label=r'$V_{er}(N)$ (стёртое)')
ax[0].semilogx(N, v_prog(N), 'r', lw=2, label=r'$V_{pr}(N)$ (записанное)')
ax[0].fill_between(N, v_erase(N), v_prog(N), color='g', alpha=0.15, label='окно программирования')
ax[0].set_xlabel('N, циклов P/E'); ax[0].set_ylabel(r'$V_{th}$, В')
ax[0].set_title('Сдвиг пороговых напряжений')
ax[0].legend(); ax[0].grid(True, which='both')
ax[1].semilogx(N, window(N), 'k', lw=2)
ax[1].axhline(W_MIN, color='r', ls='--', label=r'$W_{min}$')
ax[1].axvline(Ne, color='m', ls=':', label=f'$N_{{end}}$ = {Ne:.2e}')
ax[1].set_xlabel('N, циклов P/E'); ax[1].set_ylabel('W, В')
ax[1].set_title('Сужение окна программирования')
ax[1].legend(); ax[1].grid(True, which='both')
plt.tight_layout(); plt.savefig('b1_window.png', dpi=200); plt.close()

# Задание 2
print(f"Исходное окно W0 = {W0:.2f} В")
print(f"Ресурс (аналитически) = {endurance_analytic():.3e} циклов")
print(f"Ресурс (численно)     = {endurance_numeric():.3e} циклов")
print(f"\n{'N':>10} {'Ver, В':>8} {'Vpr, В':>8} {'W, В':>7} {'sigma, В':>9} {'n, бит':>7} {'режим':>6}")
names = {0: '--', 1: 'SLC', 2: 'MLC', 3: 'TLC', 4: 'QLC', 5: 'PLC'}
for n_ in [1e2, 1e3, 3e3, 5e3, 1e4, Ne, 3e4, 1e5]:
    w = window(n_); s = sigma(n_); nb = bits_per_cell(n_)
    print(f"{n_:10.0f} {v_erase(n_):8.2f} {v_prog(n_):8.2f} {w:7.2f} {s:9.3f} {nb:7.2f} "
          f"{names.get(int(np.floor(max(nb, 0))), 'PLC+'):>6}")

# Задание 3
nb = bits_per_cell(N)
nb_int = np.floor(np.maximum(nb, 0))
fig, ax = plt.subplots(1, 2, figsize=(12.5, 4.5))
ax[0].semilogx(N, nb, 'b', lw=2, label='непрерывная оценка')
ax[0].step(N, nb_int, 'r', lw=2, where='post', label='реализуемое число бит')
for lvl, nm in [(1, 'SLC'), (2, 'MLC'), (3, 'TLC'), (4, 'QLC')]:
    ax[0].axhline(lvl, color='gray', ls=':', lw=0.8)
    ax[0].text(1.3, lvl + 0.06, nm, color='gray', fontsize=9)
ax[0].set_xlabel('N, циклов P/E'); ax[0].set_ylabel('бит / ячейку')
ax[0].set_title('Информационная ёмкость ячейки')
ax[0].legend(); ax[0].grid(True, which='both')
cap = M_CELL * nb_int / 8 / 1e9
ax[1].semilogx(N, cap, 'g', lw=2)
ax[1].set_xlabel('N, циклов P/E'); ax[1].set_ylabel('Ёмкость, ГБ')
ax[1].set_title(f'Полезная ёмкость массива из {M_CELL:.0e} ячеек')
ax[1].grid(True, which='both')
plt.tight_layout(); plt.savefig('b2_capacity.png', dpi=200); plt.close()

# Задание 4
np.random.seed(VARIANT)
N_exp = np.array([1e2, 3e2, 1e3, 3e3, 1e4, 3e4, 1e5])
dV_true = A_E * N_exp ** BETA_E
dV_exp = dV_true * (1 + np.random.normal(0, NOISE, len(N_exp)))
A_fit, b_fit = fit_power_law(N_exp, dV_exp)
print("\nИдентификация степенного закона dV = A*N^beta:")
print(f"  истинные: A = {A_E:.4e}, beta = {BETA_E:.3f}")
print(f"  оценка:   A = {A_fit:.4e}, beta = {b_fit:.3f}")
print(f"  погрешность: dA = {abs(A_fit - A_E) / A_E * 100:.1f} %, d(beta) = {abs(b_fit - BETA_E) / BETA_E * 100:.1f} %")

plt.figure(figsize=(7, 5))
plt.loglog(N_exp, dV_exp, 'ro', ms=8, label='эксперимент')
Nf = np.logspace(2, 5.2, 100)
plt.loglog(Nf, A_fit * Nf ** b_fit, 'b-', lw=2,
           label=f'МНК: $A$={A_fit:.2e}, ' + r'$\beta$=' + f'{b_fit:.3f}')
plt.xlabel('N, циклов P/E'); plt.ylabel(r'$\Delta V_{th}$, В')
plt.title('Идентификация закона деградации')
plt.legend(); plt.grid(True, which='both')
plt.tight_layout(); plt.savefig('b3_fit.png', dpi=200); plt.close()

# Задание 5
plt.figure(figsize=(11, 4.5))
v = np.linspace(-4, 8, 2000)
for Nc, col in [(0, 'b'), (3e3, 'g'), (Ne, 'r')]:
    Nc_ = max(Nc, 1)
    w = window(Nc_); s = sigma(Nc_)
    nlev = int(2 ** np.floor(max(bits_per_cell(Nc_), 0)))
    base = v_erase(Nc_)
    step = w / max(nlev - 1, 1)
    pdf = np.zeros_like(v)
    for L in range(nlev):
        pdf += np.exp(-(v - (base + L * step)) ** 2 / (2 * s ** 2))
    plt.plot(v, pdf, col, lw=1.8,
             label=f'N={Nc:.1e}, {nlev} уровней, ' + r'$\sigma$=' + f'{s:.3f} В')
plt.xlabel(r'$V_{th}$, В'); plt.ylabel('плотность (отн. ед.)')
plt.title('Распределения порогового напряжения при циклировании')
plt.legend(); plt.grid(True)
plt.tight_layout(); plt.savefig('b4_distrib.png', dpi=200); plt.close()