import numpy as np
import matplotlib.pyplot as plt


# ЗАДАНИЕ 1-2. Параметры варианта 4 (в СИ: пА -> 1e-12 А, мА -> 1e-3 А)

I0    = 1.5e-12   # (1) ток насыщения перехода, А
n     = 1.6       # (2) коэффициент неидеальности
phiT  = 26e-3     # тепловой потенциал, В
beta  = 110.0     # (3) коэффициент передачи тока
Ua    = 100.0     # (4) напряжение Эрли, В
Uces  = 0.10      # масштаб области насыщения БТ, В
Idss  = 11e-3     # (5) ток насыщения ПТ, А
Up    = -3.0      # (6) напряжение отсечки, В
lam   = 0.025     # (7) модуляция длины канала, 1/В
Ugs_q = -1.0      # (21) рабочая точка ПТ U*_ЗИ, В

print(f"I0={I0:.2e} А, n={n}, beta={beta}, Ua={Ua} В, "
      f"Idss={Idss:.2e} А, Up={Up} В, lam={lam} 1/В, Ugs*={Ugs_q} В")


# ЗАДАНИЕ 3. Входная характеристика БТ, I_Б(0,65 В) по формуле (1)

Ube = np.linspace(0.30, 0.76, 300)              # (8) диапазон U_БЭ
Ib  = I0*(np.exp(Ube/(n*phiT)) - 1)             # (9) np.exp

Ib_formula = I0*(np.exp(0.65/(n*phiT)) - 1)     # расчёт вручную по формуле (1)
Ib_prog    = np.interp(0.65, Ube, Ib)           # значение из программы
print(f"I_Б(0.65 В): формула = {Ib_formula*1e6:.2f} мкА, "
      f"программа = {Ib_prog*1e6:.2f} мкА")

plt.figure(figsize=(6, 4))
plt.plot(Ube, Ib*1e6, lw=2)
plt.xlabel(r'$U_{БЭ}$, В'); plt.ylabel(r'$I_Б$, мкА')
plt.grid(True); plt.tight_layout(); plt.savefig('bjt_input.pdf')


# ЗАДАНИЕ 4. Выходные характеристики БТ (5 токов базы), β_диф и r_к

def bjt_ic(Uce, Ib):
    return beta*Ib*(1 - np.exp(-Uce/Uces))*(1 + Uce/Ua)   # (10)-(12)

Uce = np.linspace(0, 10, 400)
Ib_list = [10e-6, 20e-6, 30e-6, 40e-6, 50e-6]

plt.figure(figsize=(6, 4))
for Ib0 in Ib_list:
    plt.plot(Uce, bjt_ic(Uce, Ib0)*1e3, lw=2,
             label=rf'$I_Б$ = {Ib0*1e6:.0f} мкА')
plt.xlabel(r'$U_{КЭ}$, В'); plt.ylabel(r'$I_К$, мА')
plt.grid(True); plt.legend(); plt.tight_layout(); plt.savefig('bjt_output.pdf')

# параметры по формулам (3): численно
Uce_q  = 5.0
beta_d = (bjt_ic(Uce_q, 40e-6) - bjt_ic(Uce_q, 20e-6)) / (40e-6 - 20e-6)  # (19)
r_k    = (10.0 - 2.0) / (bjt_ic(10, 30e-6) - bjt_ic(2, 30e-6))            # (20)

# параметры: аналитически
beta_d_an = beta*(1 + Uce_q/Ua)      # β_диф = β(1 + U_КЭ/U_A)  (эффект Эрли)
r_k_an    = Ua/(beta*30e-6)          # r_к = U_A/(β·I_Б)

print(f"beta_диф: числ. = {beta_d:.1f}, аналит. = {beta_d_an:.1f} (beta = {beta})")
print(f"r_к: числ. = {r_k/1e3:.1f} кОм, аналит. = {r_k_an/1e3:.1f} кОм")


# ЗАДАНИЕ 5. Передаточная характеристика ПТ (U_СИ = 10 В), крутизна S

def fet_id_sat(Uds, Ugs):
    return Idss*(1 - Ugs/Up)**2*(1 + lam*Uds)           # (13)-(15)

Uds0 = 10.0
Ugs  = np.linspace(Up + 0.05, 0, 300)                   # (16)
Ids  = fet_id_sat(Uds0, Ugs)
Ic_q = fet_id_sat(Uds0, Ugs_q)

plt.figure(figsize=(6, 4))
plt.plot(Ugs, Ids*1e3, lw=2, label=r'$U_{СИ}$ = 10 В')
plt.plot([Ugs_q], [Ic_q*1e3], 'ro', label='рабочая точка')
plt.xlabel(r'$U_{ЗИ}$, В'); plt.ylabel(r'$I_С$, мА')
plt.grid(True); plt.legend(); plt.tight_layout(); plt.savefig('fet_transfer.pdf')

# крутизна: численно (полный шаг 0,1 В)
S_num = (fet_id_sat(Uds0, Ugs_q + 0.05)
         - fet_id_sat(Uds0, Ugs_q - 0.05)) / 0.1        # (22)
S_an  = 2*Idss/abs(Up) * (1 - Ugs_q/Up) * (1 + lam*Uds0)

print(f"I_С({Ugs_q} В) = {Ic_q*1e3:.2f} мА")
print(f"S: числ. = {S_num*1e3:.2f} мА/В, аналит. = {S_an*1e3:.2f} мА/В")


# ЗАДАНИЕ 6. Выходные характеристики ПТ (5 значений U_ЗИ > Up) и r_i

def fet_id(Uds, Ugs):
    Usat = Ugs - Up                                     # (17) граница областей
    b = 2*Idss/Up**2
    Ilin = b*((Ugs - Up)*Uds - Uds**2/2)                # линейная область
    Isat = fet_id_sat(Uds, Ugs)                         # насыщение
    return np.where(Uds < Usat, Ilin, Isat)             # (18)

Uds = np.linspace(0, 10, 400)
Ugs_list = np.linspace(0.9*Up, 0.15*Up, 5)   # от 0,9·Up до 0,15·Up (раздел 6)

plt.figure(figsize=(6, 4))
for u in Ugs_list:
    plt.plot(Uds, fet_id(Uds, u)*1e3, lw=2, label=rf'$U_{{ЗИ}}$ = {u:.2f} В')
plt.xlabel(r'$U_{СИ}$, В'); plt.ylabel(r'$I_С$, мА')
plt.grid(True); plt.legend(); plt.tight_layout(); plt.savefig('fet_output.pdf')

# r_i в рабочей точке: обе точки в насыщении (U_СИ >= U_ЗИ - Up = 2 В)
Usat_q = Ugs_q - Up
Uds1, Uds2 = 2.5, 10.0       # 2,5 В вместо 2 В: при 2 В точка на стыке областей
r_i    = (Uds2 - Uds1) / (fet_id(Uds2, Ugs_q) - fet_id(Uds1, Ugs_q))
r_i_an = 1 / (lam*Idss*(1 - Ugs_q/Up)**2)

print(f"Uси_нас = {Usat_q:.2f} В")
print(f"r_i: числ. = {r_i/1e3:.2f} кОм, аналит. = {r_i_an/1e3:.2f} кОм")


# ЗАДАНИЕ 7. Экспорт данных в CSV для pgfplots

np.savetxt('bjt_input.csv', np.column_stack([Ube, Ib*1e6]),
           delimiter=',', header='Ube,Ib', comments='')
np.savetxt('fet_transfer.csv', np.column_stack([Ugs, Ids*1e3]),
           delimiter=',', header='Ugs,Ids', comments='')

cols = [Uce] + [bjt_ic(Uce, ib)*1e3 for ib in Ib_list]
np.savetxt('bjt_output.csv', np.column_stack(cols), delimiter=',',
           header='Uce,' + ','.join(f'Ic{int(round(ib*1e6))}' for ib in Ib_list),
           comments='')

cols = [Uds] + [fet_id(Uds, u)*1e3 for u in Ugs_list]
np.savetxt('fet_output.csv', np.column_stack(cols), delimiter=',',
           header='Uds,' + ','.join(f'Id{k+1}' for k in range(5)), comments='')

# строки для вставки в LaTeX (легенда семейства ПТ и рабочая точка)
print(r'\foreach \c/\l in {' +
      ', '.join(f'Id{k+1}/{u:.2f}' for k, u in enumerate(Ugs_list)) + '}{')
print(f'\\addplot[only marks, mark=*, red] coordinates '
      f'{{({Ugs_q}, {Ic_q*1e3:.2f})}};')


# ЗАДАНИЕ 8 (раздел 7, п. 5 отчёта). Таблица сравнения для LaTeX

rows = [
 (r'$\beta_{диф}$ (при $U_{КЭ}=5$ В)', beta_d,    beta_d_an,  '—',    '.1f'),
 (r'$r_к$ (при $I_Б=30$ мкА)',         r_k/1e3,   r_k_an/1e3, 'кОм',  '.1f'),
 (r'$S$ (при $U_{ЗИ}=-1$ В)',          S_num*1e3, S_an*1e3,   'мА/В', '.2f'),
 (r'$r_i$ (при $U_{ЗИ}=-1$ В)',        r_i/1e3,   r_i_an/1e3, 'кОм',  '.2f'),
]
print(r'\begin{tabular}{lccc}\hline')
print(r'Параметр & Численно & Аналитически & Ед. \\ \hline')
for name, a, b, u, f in rows:
    print(f'{name} & {a:{f}} & {b:{f}} & {u} \\\\')
print(r'\hline\end{tabular}')

plt.show()