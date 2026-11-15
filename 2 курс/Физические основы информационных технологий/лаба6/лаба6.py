import math
from statistics import NormalDist
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(2026)

VDD = 1.10          # В, напряжение питания
CS = 20e-15         # Ф, ёмкость накопительного конденсатора
CBL = 180e-15       # Ф, ёмкость разрядной линии
RON = 8e3           # Ом, сопротивление открытого канала
RLEAK = 150e12      # Ом, эквивалентное сопротивление утечки
I0 = 0.04e-15       # А, постоянная составляющая тока утечки
DVMIN = 35e-3       # В, чувствительность усилителя считывания
T0 = 45.0           # °C, опорная температура
DT2 = 10.0          # °C, удвоение тока утечки
NROWS = 65536       # число строк в банке
TRFC = 350e-9       # с, длительность команды REF
RBURST = 8          # строк за одну команду REF
KSAFE = 2.0         # коэффициент запаса
SIG_LN = 0.95       # СКО логнормального распределения
NCELLS = 10**6      # число ячеек в статистической модели
LAM_HL = 1 / 600    # 1/с, интенсивность перехода high -> low (VRT)
LAM_LH = 1 / 60     # 1/с, интенсивность перехода low -> high (VRT)
RATIO_VRT = 4.0     # во сколько раз t_low меньше t_high (VRT)
T_HOUR = 3600.0     # с, время наблюдения (VRT)
N_VRT = 2000        # число ячеек в модели VRT

TAU_W = RON * CS
TAU_LEAK = RLEAK * CS
KAPPA = CBL / CS
Q = CS * VDD
VC_MIN = VDD / 2 + DVMIN * (1 + KAPPA)

erfc_v = np.vectorize(math.erfc)

def eng(x, unit=''):
    if x == 0:
        return f'0 {unit}'
    pref = [(1e12, 'Т'), (1e9, 'Г'), (1e6, 'М'), (1e3, 'к'), (1, ''),
            (1e-3, 'м'), (1e-6, 'мк'), (1e-9, 'н'), (1e-12, 'п'), (1e-15, 'ф')]
    for m, p in pref:
        if abs(x) >= m:
            return f'{x / m:.3g} {p}{unit}'
    return f'{x:.3e} {unit}'

def rk4(f, y0, t):
    y = np.empty(len(t))
    y[0] = y0
    for i in range(len(t) - 1):
        h = t[i + 1] - t[i]
        k1 = f(t[i], y[i])
        k2 = f(t[i] + h / 2, y[i] + h * k1 / 2)
        k3 = f(t[i] + h / 2, y[i] + h * k2 / 2)
        k4 = f(t[i] + h, y[i] + h * k3)
        y[i + 1] = y[i] + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6
    return y

def write_analytic(t, v_start, v_target):
    return v_target + (v_start - v_target) * np.exp(-t / TAU_W)

def write_numeric(t_end, v_start, v_target, n=4000):
    t = np.linspace(0, t_end, n)
    return t, rk4(lambda tt, v: (v_target - v) / TAU_W, v_start, t)

def leak_exp(t, v0=VDD):
    return v0 * np.exp(-t / TAU_LEAK)

def leak_lin(t, v0=VDD):
    return np.maximum(v0 - I0 * t / CS, 0.0)

def leak_mixed(t, v0=VDD, scale=1.0):
    i0 = I0 * scale
    r = RLEAK / scale
    return (v0 + i0 * r) * np.exp(-t / (r * CS)) - i0 * r

def leak_numeric(t_end, v0=VDD, scale=1.0, n=5000):
    t = np.linspace(0, t_end, n)
    return t, rk4(lambda tt, v: -(I0 * scale + v * scale / RLEAK) / CS, v0, t)

def dv_bl(vc):
    return CS / (CS + CBL) * (vc - VDD / 2)

def temp_scale(T):
    return 2.0 ** ((T - T0) / DT2)

def retention_analytic(T=T0):
    return TAU_LEAK / temp_scale(T) * np.log(VDD / VC_MIN)

def retention_numeric(T=T0):
    sc = temp_scale(T)
    lo, hi = 1e-9, 1000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if leak_mixed(mid, scale=sc) - VC_MIN > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2

def refresh_params(t_ret):
    t_ref = t_ret / KSAFE
    n_ref = NROWS / RBURST
    t_refi = t_ref / n_ref
    eta = n_ref * TRFC / t_ref * 100
    e = NCELLS * CS * VDD ** 2 * 0.5
    return dict(t_ref=t_ref, n_ref=n_ref, t_refi=t_refi, eta=eta, E=e, P=e / t_ref)

def lognorm_cdf(t, mu, sig):
    return 0.5 * erfc_v(-(np.log(t) - mu) / (sig * math.sqrt(2.0)))

def vrt_fail_probability(t_high, k_safe, n=N_VRT, horizon=T_HOUR):
    t_low = t_high / RATIO_VRT
    delta = t_high / k_safe
    n_int = int(horizon / delta)
    p_low = LAM_HL / (LAM_HL + LAM_LH)
    low = np.random.rand(n) < p_low
    failed = np.zeros(n, dtype=bool)
    p_hl = 1 - math.exp(-LAM_HL * delta)
    p_lh = 1 - math.exp(-LAM_LH * delta)
    for _ in range(n_int):
        sw = np.random.rand(n) < np.where(low, p_lh, p_hl)
        tau1 = np.where(sw, np.random.rand(n) * delta, delta)
        r_cur = np.where(low, 1 / t_low, 1 / t_high)
        r_new = np.where(low, 1 / t_high, 1 / t_low)
        u = tau1 * r_cur + (delta - tau1) * r_new * sw
        failed |= u >= 1.0
        low = low ^ sw
    return failed.mean()

# Задание 1
t_ret_an = retention_analytic()
p0 = refresh_params(t_ret_an)
print(f'tau_w = {eng(TAU_W, "с")}, t(10-90%) = {eng(TAU_W * math.log(9), "с")}')
print(f'Q = {eng(Q, "Кл")} ({Q / 1.602e-19:.3e} электронов)')
print(f'kappa = {KAPPA:.1f}, dV_BL("1") = {eng(dv_bl(VDD), "В")}, dV_BL("0") = {eng(dv_bl(0.0), "В")}')
print(f'Vc_min = {VC_MIN:.4f} В, допустимая потеря заряда = {(VDD - VC_MIN) / VDD * 100:.1f} %')
print(f'tau_leak = {eng(TAU_LEAK, "с")}, t_RET (аналитика) = {eng(t_ret_an, "с")}')
print(f't_REF = {eng(p0["t_ref"], "с")}, t_REFI = {eng(p0["t_refi"], "с")}, eta = {p0["eta"]:.2f} %')

# Задание 2
t_end = 6 * TAU_W
t = np.linspace(0, t_end, 2000)
v1_an = write_analytic(t, 0.0, VDD)
v0_an = write_analytic(t, VDD, 0.0)
t1_n, v1_n = write_numeric(t_end, 0.0, VDD)
t0_n, v0_n = write_numeric(t_end, VDD, 0.0)
err1 = np.max(np.abs(v1_n - write_analytic(t1_n, 0.0, VDD)))
print(f'\nМакс. расхождение числ./аналит. = {err1:.3e} В')
print(f't(10-90%) = {eng(TAU_W * math.log(9), "с")}')
print(f't(0-90%) = {eng(-TAU_W * math.log(0.1), "с")}')
print(f't(0-99%) = {eng(-TAU_W * math.log(0.01), "с")}')

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
ax[0].plot(t * 1e9, v1_an, color='#1E5AB4', lw=2.5, label='аналитика, запись "1"')
ax[0].plot(t1_n * 1e9, v1_n, 'o', ms=3, color='#C82828', markevery=90, label='численно (RK4)')
ax[0].plot(t * 1e9, v0_an, color='#148C3C', lw=2.5, label='аналитика, запись "0"')
ax[0].plot(t0_n * 1e9, v0_n, 's', ms=3, color='#E68C14', markevery=90, label='численно (RK4)')
ax[0].axhline(0.9 * VDD, ls='--', c='gray', lw=1)
ax[0].axhline(0.1 * VDD, ls='--', c='gray', lw=1)
ax[0].set_xlabel('t, нс'); ax[0].set_ylabel('$V_C$, В')
ax[0].set_title('Переходные процессы записи')
ax[0].legend(fontsize=9); ax[0].grid(alpha=0.3)
i1 = (VDD - v1_an) / RON
ax[1].plot(t * 1e9, i1 * 1e6, color='#1E5AB4', lw=2.5)
ax[1].set_xlabel('t, нс'); ax[1].set_ylabel('I, мкА')
ax[1].set_title('Ток заряда через ключевой транзистор')
ax[1].grid(alpha=0.3)
q_int = float(np.sum((i1[1:] + i1[:-1]) / 2 * np.diff(t)))
print(f'Интеграл тока за 6*tau_w = {eng(q_int, "Кл")}, Cs*VDD = {eng(Q, "Кл")}, пиковый ток = {eng(VDD / RON, "А")}')
ax[1].text(0.45, 0.8, f'$\\int I\\,dt$ = {eng(q_int, "Кл")}\n$C_sV_{{DD}}$ = {eng(Q, "Кл")}',
           transform=ax[1].transAxes, bbox=dict(fc='w', alpha=0.85))
plt.tight_layout(); plt.savefig('fig1_write.png', dpi=200); plt.close()

# Задание 3
tl = np.linspace(0, 1.5, 4000)
ve = leak_exp(tl)
vl = leak_lin(tl)
vm = leak_mixed(tl)
tn, vn = leak_numeric(1.5)
print(f'\n{"модель":<22}{"V(0.1 с)":>10}{"V(0.3 с)":>10}{"V(0.6 с)":>10}{"V(1.0 с)":>10}')
for name, f in [('экспоненциальная', leak_exp), ('линейная (I0)', leak_lin), ('комбинированная', leak_mixed)]:
    print(f'{name:<22}' + ''.join(f'{float(f(x)):10.4f}' for x in (0.1, 0.3, 0.6, 1.0)))

plt.figure(figsize=(8, 5))
plt.plot(tl, ve, lw=2.5, color='#1E5AB4', label=r'экспон.: $V_{DD}e^{-t/\tau}$')
plt.plot(tl, vl, lw=2.5, color='#148C3C', label=r'линейн.: $V_{DD}-I_0t/C_s$')
plt.plot(tl, vm, lw=2.5, color='#C82828', label='комбинированная')
plt.plot(tn, vn, 'k--', lw=1.2, label='числ. решение ОДУ')
plt.axhline(VC_MIN, color='#E68C14', ls='-.', lw=2, label=f'$V_{{C,min}}$ = {VC_MIN:.3f} В')
plt.axhline(VDD / 2, color='gray', ls=':', lw=1.5, label='$V_{DD}/2$')
plt.xlabel('t, с'); plt.ylabel('$V_C$, В')
plt.title('Разряд ячейки в режиме хранения')
plt.legend(fontsize=8.5); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('fig2_leak.png', dpi=200); plt.close()

# Задание 4
tret = retention_numeric()
print(f'\nt_RET (аналитически, экспоненциальная модель) = {eng(retention_analytic(), "с")}')
print(f't_RET (численно, комбинированная модель)      = {eng(tret, "с")}')
tl2 = np.linspace(0, 1.0, 4000)
d_sig = dv_bl(leak_mixed(tl2)) * 1e3

plt.figure(figsize=(8, 5))
plt.plot(tl2, d_sig, lw=2.5, color='#1E5AB4')
plt.axhline(DVMIN * 1e3, color='#C82828', ls='--', lw=2, label=f'$\\Delta V_{{min}}$ = {DVMIN * 1e3:.0f} мВ')
plt.axvline(tret, color='#148C3C', ls=':', lw=2, label=f'$t_{{RET}}$ = {tret:.3f} с')
plt.fill_between(tl2, DVMIN * 1e3, d_sig, where=d_sig > DVMIN * 1e3, color='#148C3C', alpha=0.15)
plt.xlabel('t, с'); plt.ylabel(r'$\Delta V_{BL}$, мВ')
plt.title('Сигнал на разрядной линии')
plt.legend(fontsize=9); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('fig3_dvbl.png', dpi=200); plt.close()

# Задание 5
Tgrid = np.linspace(0, 105, 300)
tret_T = np.array([retention_numeric(T) for T in Tgrid])
print(f'\n{"T, °C":>7}{"множитель":>12}{"t_RET":>14}{"режим":>16}')
for T in [0, 25, 45, 55, 85, 95, 105]:
    tr = retention_numeric(T)
    mode = '2x refresh' if T > 85 else 'норм. 1x'
    print(f'{T:>7.0f}{temp_scale(T):>12.3f}{eng(tr, "с"):>14}{mode:>16}')
t85, t95 = retention_numeric(85), retention_numeric(95)

plt.figure(figsize=(8, 5))
plt.semilogy(Tgrid, tret_T * 1e3, lw=2.8, color='#1E5AB4')
plt.plot([85, 95], [t85 * 1e3, t95 * 1e3], 'ro')
plt.axhline(64, color='#C82828', ls='--', lw=2, label='JEDEC $t_{REFW}$ = 64 мс (DDR4)')
plt.axhline(32, color='#E68C14', ls='--', lw=2, label='JEDEC $t_{REFW}$ = 32 мс (DDR5)')
plt.axvline(85, color='gray', ls=':', lw=2, label='граница 2x refresh')
plt.xlabel('T, °C'); plt.ylabel('$t_{RET}$, мс')
plt.title('Зависимость времени хранения от температуры')
plt.legend(fontsize=9); plt.grid(alpha=0.3, which='both')
plt.tight_layout(); plt.savefig('fig4_temp.png', dpi=200); plt.close()

# Задание 6
med = retention_numeric()
mu = math.log(med)
sample = np.random.lognormal(mu, SIG_LN, NCELLS)
print(f'\nмедиана t_RET = {eng(med, "с")}, минимум в выборке = {eng(sample.min(), "с")}')
for p in [50, 10, 1, 0.1, 0.01, 0.001]:
    print(f'{p:>7.3f} %-й процентиль = {eng(np.percentile(sample, p), "с")}')
nd = NormalDist()
t_need = {}
for pf in [1e-3, 1e-6, 1e-9, 1e-12]:
    t_need[pf] = math.exp(mu + nd.inv_cdf(pf) * SIG_LN)
    print(f'P_fail = {pf:6.0e} -> t_REF <= {eng(t_need[pf], "с")}')
print(f'Запас: медиана / t_REF(1e-9) = {med / t_need[1e-9]:.0f}')

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
ax[0].hist(sample * 1e3, bins=np.logspace(0, 5, 120), color='#1E5AB4', alpha=0.75, edgecolor='none')
ax[0].set_xscale('log')
ax[0].axvline(med * 1e3, color='#C82828', lw=2.5, label=f'медиана {med * 1e3:.0f} мс')
ax[0].axvline(t_need[1e-9] * 1e3, color='#148C3C', lw=2.5, ls='--', label=f'$P_{{fail}}=10^{{-9}}$: {t_need[1e-9] * 1e3:.1f} мс')
ax[0].set_xlabel('$t_{RET}$, мс'); ax[0].set_ylabel('число ячеек')
ax[0].set_title(f'Распределение $t_{{RET}}$ ($N = 10^{{{int(math.log10(NCELLS))}}}$)')
ax[0].legend(fontsize=9); ax[0].grid(alpha=0.3)
tgrid = np.logspace(-4, 1, 400)
cdf = lognorm_cdf(tgrid, mu, SIG_LN)
ax[1].loglog(tgrid * 1e3, np.maximum(cdf, 1e-16), lw=2.8, color='#1E5AB4')
for pf, col in [(1e-3, '#E68C14'), (1e-6, '#148C3C'), (1e-9, '#C82828')]:
    ax[1].axhline(pf, ls='--', lw=1.5, color=col, label=f'$P_{{fail}}$ = {pf:.0e}')
ax[1].set_xlabel('$t_{REF}$, мс'); ax[1].set_ylabel('доля отказавших ячеек')
ax[1].set_title('Вероятность отказа vs период регенерации')
ax[1].set_ylim(1e-14, 1); ax[1].legend(fontsize=9); ax[1].grid(alpha=0.3, which='both')
plt.tight_layout(); plt.savefig('fig5_stat.png', dpi=200); plt.close()

# Задание 7
bases = [('по медиане', med), ('по 85 °C', t85), ('по 95 °C', t95), ('по худшей ячейке (P=1e-9)', t_need[1e-9])]
for label, tr in bases:
    p = refresh_params(tr)
    print(f'\n--- {label}: t_RET = {eng(tr, "с")} ---')
    print(f'  окно t_REFW = {eng(p["t_ref"], "с")}, команд REF = {p["n_ref"]:.0f}, t_REFI = {eng(p["t_refi"], "с")}')
    print(f'  накладные eta = {p["eta"]:.2f} %, E_REF = {eng(p["E"], "Дж")}, мощность = {eng(p["P"], "Вт")}')

rows = np.logspace(10, 18, 200, base=2)
plt.figure(figsize=(8, 5))
for (label, tr), col in zip(bases, ['#1E5AB4', '#E68C14', '#148C3C', '#C82828']):
    eta = rows / RBURST * TRFC / (tr / KSAFE) * 100
    plt.plot(rows, np.minimum(eta, 100), lw=2.5, color=col, label=label)
plt.xscale('log', base=2)
plt.axhline(10, ls='--', c='gray', label='практический предел 10 %')
plt.axvline(NROWS, ls=':', c='k', lw=1.2)
plt.xlabel('Число строк в банке'); plt.ylabel(r'$\eta_{REF}$, %')
plt.title('Накладные расходы на регенерацию')
plt.ylim(0, 105); plt.legend(fontsize=9); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('fig6_refresh.png', dpi=200); plt.close()

# Задание 8
t_refresh = med / KSAFE
t_tot, v_tot, wl = [], [], []
tc, vc = 0.0, 0.0

tw = np.linspace(0, 5 * TAU_W, 300)
vw = write_analytic(tw, 0.0, VDD)
t_tot += list(tc + tw); v_tot += list(vw); wl += [1] * len(tw)
tc += tw[-1]; vc = vw[-1]

for step in range(2):
    ts = np.linspace(0, t_refresh, 800)
    vs = leak_mixed(ts, v0=vc)
    t_tot += list(tc + ts); v_tot += list(vs); wl += [0] * len(ts)
    tc += t_refresh; vc = vs[-1]
    if step == 0:
        tr_ = np.linspace(0, 5 * TAU_W, 120)
        vr = write_analytic(tr_, vc, VDD)
        t_tot += list(tc + tr_); v_tot += list(vr); wl += [1] * len(tr_)
        tc += tr_[-1]; vc = vr[-1]
t_read = tc
print(f'\nСчитывание на t = {eng(t_read, "с")}: V_C = {vc:.4f} В, dV_BL = {eng(dv_bl(vc), "В")} (порог {eng(DVMIN, "В")})')
tr_ = np.linspace(0, 5 * TAU_W, 120)
vr = write_analytic(tr_, vc, VDD)
t_tot += list(tc + tr_); v_tot += list(vr); wl += [1] * len(tr_)
tc += tr_[-1]; vc = vr[-1]

ts = np.linspace(0, 3 * med, 1200)
vs = leak_mixed(ts, v0=vc)
t_tot += list(tc + ts); v_tot += list(vs); wl += [0] * len(ts)
t_tot = np.array(t_tot); v_tot = np.array(v_tot); wl = np.array(wl)

fig, ax = plt.subplots(2, 1, figsize=(13, 6.5), sharex=True, gridspec_kw={'height_ratios': [1, 3]})
ax[0].fill_between(t_tot, 0, wl, step='post', color='#1E5AB4', alpha=0.6)
ax[0].set_ylabel('WL'); ax[0].set_yticks([0, 1]); ax[0].set_yticklabels(['0', '$V_{PP}$'])
ax[0].grid(alpha=0.3)
ax[1].plot(t_tot, v_tot, lw=2.2, color='#1E5AB4')
ax[1].axhline(VC_MIN, color='#C82828', ls='--', lw=2, label='$V_{C,min}$')
ax[1].axhline(VDD / 2, color='gray', ls=':', lw=1.5, label='$V_{DD}/2$')
ax[1].fill_between(t_tot, 0, VDD, where=v_tot < VC_MIN, color='#C82828', alpha=0.12, label='данные потеряны')
for tm, nm in [(0.0, 'запись "1"'), (t_refresh, 'регенерация'), (t_read, 'считывание + restore')]:
    ax[1].axvline(tm, color='k', ls=':', lw=1)
    ax[1].text(tm, 0.05, nm, rotation=90, va='bottom', ha='right', fontsize=9)
ax[1].set_xlabel('t, с'); ax[1].set_ylabel('$V_C$, В')
ax[1].legend(fontsize=9, loc='upper right'); ax[1].grid(alpha=0.3)
plt.suptitle('Полный цикл: запись -> хранение -> регенерация -> хранение -> считывание -> отказ')
plt.tight_layout(); plt.savefig('fig7_cycle.png', dpi=200); plt.close()

# Задание 9
kap = np.linspace(2, 30, 300)
dv = 0.5 * VDD / (1 + kap)
k_lim = (VDD / 2) / DVMIN - 1
print(f'\nПредельное kappa при dVmin = {DVMIN * 1e3:.0f} мВ: {k_lim:.2f}')
print(f'Текущее kappa = {KAPPA:.2f} ({"OK" if KAPPA < k_lim else "НЕ ПРОХОДИТ"}), запас по сигналу {(dv_bl(VDD) - DVMIN) * 1e3:.1f} мВ')

plt.figure(figsize=(8, 5))
plt.plot(kap, dv * 1e3, lw=2.8, color='#1E5AB4')
plt.axhline(DVMIN * 1e3, color='#C82828', ls='--', lw=2, label=r'$\Delta V_{min}$')
plt.axvline(KAPPA, color='#148C3C', ls=':', lw=2, label=f'текущее $\\kappa$ = {KAPPA:.0f}')
plt.axvline(k_lim, color='#E68C14', ls='-.', lw=2, label=f'предел $\\kappa$ = {k_lim:.1f}')
plt.xlabel(r'$\kappa = C_{BL}/C_s$'); plt.ylabel(r'$\Delta V_{BL}$, мВ')
plt.title('Сигнал считывания vs отношение ёмкостей')
plt.legend(fontsize=9); plt.grid(alpha=0.3)
plt.tight_layout(); plt.savefig('fig8_kappa.png', dpi=200); plt.close()

# Задание 10
t_high = retention_numeric()
t_low = t_high / RATIO_VRT
p_low_stat = LAM_HL / (LAM_HL + LAM_LH)
print(f'\nVRT: t_high = {eng(t_high, "с")}, t_low = {eng(t_low, "с")}, доля времени в low = {p_low_stat * 100:.1f} %')
ks = [2, 3, 5, 8]
pfail = []
for k in ks:
    pf = vrt_fail_probability(t_high, k)
    pfail.append(pf)
    print(f'k_safe = {k}: t_REF = {eng(t_high / k, "с")}, P_fail за 1 час = {pf:.3f}')

t_ev, s_ev, tcur, low = [0.0], [], 0.0, np.random.rand() < p_low_stat
while tcur < T_HOUR:
    dwell = np.random.exponential(1 / (LAM_LH if low else LAM_HL))
    s_ev.append(t_low if low else t_high)
    tcur += dwell
    t_ev.append(min(tcur, T_HOUR))
    low = not low

fig, ax = plt.subplots(1, 2, figsize=(13, 4.6))
ax[0].step(np.array(t_ev) / 60, np.append(np.array(s_ev), s_ev[-1]) * 1e3, where='post', lw=2, color='#1E5AB4')
ax[0].axhline(t_high / KSAFE * 1e3, color='#C82828', ls='--', lw=2, label=f'$t_{{REF}}$ при $k_{{safe}}$ = {KSAFE:.0f}')
ax[0].set_xlabel('t, мин'); ax[0].set_ylabel('$t_{RET}$ ячейки, мс')
ax[0].set_title('VRT: переключение ячейки между состояниями')
ax[0].legend(fontsize=9); ax[0].grid(alpha=0.3)
ax[1].bar([str(k) for k in ks], pfail, color='#1E5AB4')
ax[1].set_xlabel('$k_{safe}$'); ax[1].set_ylabel('$P_{fail}$ за 1 час')
ax[1].set_title('Вероятность отказа VRT-ячейки')
ax[1].grid(alpha=0.3, axis='y')
plt.tight_layout(); plt.savefig('fig9_vrt.png', dpi=200); plt.close()