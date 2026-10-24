import numpy as np
import matplotlib.pyplot as plt

# ===== ЗАДАНИЕ 1. Параметры варианта 4 (таблица 2), перевод в СИ =====
E    = 6.0          # (1) напряжение питания, В
Rb   = 20e3         # (2) резистор базы, Ом
Rc   = 1.0e3        # (3) резистор коллектора, Ом
beta = 150          # (4) коэффициент усиления БТ
Ube, Uces = 0.6, 0.1
Utn  = 0.7          # (5) порог NMOS, В
Utp  = -0.7         # (6) порог PMOS, В (отрицательный)
kn   = 5.0e-3       # (7) крутизна NMOS, А/В²
kp   = 2.5e-3       # (8) крутизна PMOS, А/В²
Rn   = 55.0         # (9) сопротивление открытого NMOS, Ом
Rp   = 110.0        # (10) сопротивление открытого PMOS, Ом
Cl   = 75e-12       # (11) ёмкость нагрузки, Ф
T    = 25e-9        # тактовый интервал, с

# ===== ЗАДАНИЕ 3. Передаточная характеристика РТЛ-ключа =====
def rtl_out(Uin):
    if Uin < Ube:                       # (12)
        return E
    Ib = (Uin - Ube) / Rb               # (13)
    Ic = beta * Ib                      # (14)
    return max(E - Ic * Rc, Uces)       # (15), (16)

Uin = np.linspace(0, E, 400)
Uout_rtl = np.array([rtl_out(u) for u in Uin])
Uth_rtl = np.interp(E/2, Uout_rtl[::-1], Uin[::-1])
Uth_rtl_f = Ube + E*Rb/(2*beta*Rc)
Uin_sat_f = Ube + (E - Uces)*Rb/(beta*Rc)
Ib_work = (E - Ube) / Rb
Ib_sat  = (E - Uces) / (beta * Rc)

print(f"U_пор РТЛ: числ. {Uth_rtl:.3f} В, формула (2) {Uth_rtl_f:.3f} В")
print(f"U_вх,нас = {Uin_sat_f:.3f} В")
print(f"Iб(Uвх=E) = {Ib_work*1e6:.1f} мкА, Iб_нас = {Ib_sat*1e6:.1f} мкА -> "
      f"{'насыщен' if Ib_work > Ib_sat else 'НЕ насыщен'}")
print(f"Статический ток РТЛ при Uвх=E: {(E-Uces)/Rc*1e3:.2f} мА")

plt.figure(figsize=(6, 4))
plt.plot(Uin, Uout_rtl, lw=2)
plt.axhline(E/2, color='gray', ls='--', lw=1)
plt.plot([Uth_rtl], [E/2], 'ro')
plt.xlabel('Uвх, В'); plt.ylabel('Uвых, В')
plt.grid(True); plt.tight_layout()
plt.savefig('rtl_vtc.png', dpi=200); plt.close()

# ===== ЗАДАНИЕ 4. Передаточная характеристика КМОП-инвертора =====
def mos_n(Ugs, Uds):
    if Ugs < Utn:
        return 0.0
    if Uds >= Ugs - Utn:
        return (kn/2) * (Ugs - Utn)**2                  # (17)
    return kn * ((Ugs - Utn)*Uds - Uds**2/2)            # (18)

def mos_p(Uin_, Uout_):
    Usg, Usd = E - Uin_, E - Uout_
    if Usg < abs(Utp):                                  # (19)
        return 0.0
    if Usd >= Usg - abs(Utp):
        return (kp/2) * (Usg - abs(Utp))**2
    return kp * ((Usg - abs(Utp))*Usd - Usd**2/2)

def cmos_out(Uin_):
    grid = np.linspace(0, E, 2001)
    diff = [abs(mos_n(Uin_, u) - mos_p(Uin_, u)) for u in grid]
    return grid[np.argmin(diff)]                        # (20)

Uout_cmos = np.array([cmos_out(u) for u in Uin])
Uth_cmos = np.interp(E/2, Uout_cmos[::-1], Uin[::-1])
q = np.sqrt(kp/kn)
Uth_cmos_f = (Utn + q*(E - abs(Utp))) / (1 + q)
I_th = kn/2 * (Uth_cmos_f - Utn)**2

print(f"U_пор КМОП: числ. {Uth_cmos:.3f} В, формула (4) {Uth_cmos_f:.3f} В, E/2 = {E/2:.2f} В")
print(f"kn = {kn*1e3:.2f} мА/В², kp = {kp*1e3:.2f} мА/В², sqrt(kp/kn) = {q:.3f}")
print(f"Сквозной ток в точке переключения: {I_th*1e3:.2f} мА")

plt.figure(figsize=(6, 4))
plt.plot(Uin, Uout_cmos, lw=2)
plt.axhline(E/2, color='gray', ls='--', lw=1)
plt.plot([Uth_cmos], [E/2], 'ro')
plt.xlabel('Uвх, В'); plt.ylabel('Uвых, В')
plt.grid(True); plt.tight_layout()
plt.savefig('cmos_vtc.png', dpi=200); plt.close()

# ===== ЗАДАНИЕ 5. Переходные процессы и задержки =====
tau_n = Rn * Cl                                         # (21)
tau_p = Rp * Cl                                         # (22)
t = np.linspace(0, 8*max(tau_n, tau_p), 4000)
u_fall = E * np.exp(-t / tau_n)                         # (23)
u_rise = E * (1 - np.exp(-t / tau_p))                   # (24), (25)

t_pHL = np.log(2) * tau_n
t_pLH = np.log(2) * tau_p                               # (26)
t_p   = (t_pHL + t_pLH) / 2                             # (27)
t_r   = np.log(9) * tau_p
t_f   = np.log(9) * tau_n

tHL_m = np.interp(E/2, u_fall[::-1], t[::-1])
tLH_m = np.interp(E/2, u_rise, t)
tp_m  = (tHL_m + tLH_m) / 2
tr_m  = np.interp(0.9*E, u_rise, t) - np.interp(0.1*E, u_rise, t)
tf_m  = np.interp(0.1*E, u_fall[::-1], t[::-1]) - np.interp(0.9*E, u_fall[::-1], t[::-1])

rows = [("U_пор РТЛ, В", Uth_rtl_f, Uth_rtl),
        ("U_пор КМОП, В", Uth_cmos_f, Uth_cmos),
        ("t_pHL, нс", t_pHL*1e9, tHL_m*1e9),
        ("t_pLH, нс", t_pLH*1e9, tLH_m*1e9),
        ("t_p, нс",   t_p*1e9,   tp_m*1e9),
        ("t_r, нс",   t_r*1e9,   tr_m*1e9),
        ("t_f, нс",   t_f*1e9,   tf_m*1e9)]
print(f"tau_n = {tau_n*1e9:.3f} нс, tau_p = {tau_p*1e9:.3f} нс")
print(f"{'Параметр':<16}{'Аналитика':>12}{'Числ. экс.':>12}")
for name, a, m in rows:
    print(f"{name:<16}{a:>12.3f}{m:>12.3f}")

plt.figure(figsize=(6, 4))
plt.plot(t*1e9, u_fall, lw=2, label='спад')
plt.plot(t*1e9, u_rise, lw=2, label='фронт')
plt.axhline(E/2, color='gray', ls='--', lw=1)
plt.xlabel('t, нс'); plt.ylabel('Uвых, В')
plt.grid(True); plt.legend(); plt.tight_layout()
plt.savefig('delay.png', dpi=200); plt.close()

# ===== ЗАДАНИЯ 6, 7. Временные диаграммы И и ИЛИ =====
def simulate_gate(func, seqA, seqB, n_per=2000):
    N = len(seqA)
    t2 = np.linspace(0, N*T, N*n_per + 1)
    idx = np.minimum((t2 // T).astype(int), N - 1)
    A = np.array(seqA, float)[idx]
    B = np.array(seqB, float)[idx]
    Yideal = func(A, B)                                  # (30)
    dt = t2[1] - t2[0]
    Y1 = np.zeros_like(t2); Y = np.zeros_like(t2)
    Y1[0] = E * (1 - Yideal[0]); Y[0] = E * Yideal[0]
    for k in range(1, len(t2)):
        # 1-й каскад: И-НЕ (ИЛИ-НЕ)
        tgt1 = E * (1 - Yideal[k])
        tau1 = tau_n if tgt1 < 0.5*E else tau_p          # (28), (29)
        Y1[k] = Y1[k-1] + dt/tau1 * (tgt1 - Y1[k-1])
        # 2-й каскад: НЕ
        high = Y1[k] > E/2
        tgt2 = 0.0 if high else E
        tau2 = tau_n if high else tau_p
        Y[k] = Y[k-1] + dt/tau2 * (tgt2 - Y[k-1])
    return t2, A, B, Yideal, Y

def measure_delays(t2, Yideal, Y):
    res = []
    for k in range(1, int(round(t2[-1]/T))):
        i0 = int(np.searchsorted(t2, k*T))
        i1 = int(np.searchsorted(t2, (k+1)*T))
        if Yideal[i0] == Yideal[i0-1]:
            continue
        rising = Yideal[i0] > Yideal[i0-1]
        seg = Y[i0:i1]
        hit = np.where(seg >= E/2)[0] if rising else np.where(seg <= E/2)[0]
        d = (t2[i0 + hit[0]] - k*T) if len(hit) else np.nan
        res.append(('LH' if rising else 'HL', k*T, d))
    return res

seqA = [0, 0, 1, 1, 0]   # 00, 01, 10, 11 (+ 00 для измерения спада)
seqB = [0, 1, 0, 1, 0]

def run_gate(name, tag, func):
    t2, A, B, Yi, Y = simulate_gate(func, seqA, seqB)
    print(f"--- Элемент {name}: теория по (7): "
          f"tpLH = {(t_pHL+t_pLH)*1e9:.3f} нс, tpHL = {(t_pLH+t_pHL)*1e9:.3f} нс")
    for kind, tedge, d in measure_delays(t2, Yi, Y):
        print(f"  перепад {kind} при t = {tedge*1e9:.0f} нс: измеренная задержка {d*1e9:.3f} нс")
    plt.figure(figsize=(7, 4))
    plt.step(t2*1e9, A*1.2*E/2 + 2.4*E, where='post', label='A')
    plt.step(t2*1e9, B*1.2*E/2 + 1.2*E, where='post', label='B')
    plt.step(t2*1e9, Yi*E, where='post', color='gray', label=f'Y ({name}) идеал')
    plt.plot(t2*1e9, Y, lw=2, label=f'Y ({name})')
    plt.xlabel('t, нс'); plt.grid(True); plt.legend()
    plt.tight_layout(); plt.savefig(f'timing_{tag}.png', dpi=200); plt.close() 
    np.savetxt(f'timing_{tag}.csv',
               np.column_stack([t2[::10]*1e9, A[::10], B[::10], Yi[::10]*E, Y[::10]]),
               delimiter=',', header='t,A,B,Yideal,Y', comments='')

run_gate("И", "and", lambda a, b: a*b)                       # задание 6
run_gate("ИЛИ", "or", lambda a, b: np.maximum(a, b))         # задание 7

# ===== ЗАДАНИЕ 8. Экспорт в CSV =====
np.savetxt('cmos_vtc.csv', np.column_stack([Uin, Uout_cmos]),
           delimiter=',', header='Uin,Uout', comments='')
np.savetxt('rtl_vtc.csv', np.column_stack([Uin, Uout_rtl]),
           delimiter=',', header='Uin,Uout', comments='')
np.savetxt('delay.csv', np.column_stack([t[::4]*1e9, u_fall[::4], u_rise[::4]]),
           delimiter=',', header='t,Ufall,Urise', comments='')