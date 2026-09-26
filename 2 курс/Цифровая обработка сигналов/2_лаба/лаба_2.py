import os
import numpy as np
import matplotlib.pyplot as plt

SAVE_DIR = r"E:\NCFU\2 курс\Цифровая обработка сигналов\2_лаба"
os.makedirs(SAVE_DIR, exist_ok=True)

# ---------- общие параметры (вариант 4) ----------
f0 = 50
A = 1.0
fs_hi = 20000
t_hi = np.arange(0, 0.2, 1/fs_hi)
x_hi = A * np.sin(2*np.pi*f0*t_hi)

# ---------- Задание 1 ----------
plt.figure(figsize=(9, 3))
plt.plot(t_hi*1000, x_hi)
plt.title(f'Высокочастотная синусоида, f0 = {f0} Гц')
plt.xlabel('t, мс'); plt.ylabel('x(t)')
plt.grid(alpha=0.3)
plt.savefig(os.path.join(SAVE_DIR, 'task1_signal.png'), dpi=150, bbox_inches='tight')

# ---------- Задание 2 ----------
fs = 500
t_s = np.arange(0, 0.2, 1/fs)
x_s = A * np.sin(2*np.pi*f0*t_s)
plt.figure(figsize=(9, 3))
plt.plot(t_hi*1000, x_hi, color='gray', alpha=0.6, label='"аналоговый" сигнал')
plt.stem(t_s*1000, x_s, linefmt='C0-', markerfmt='C0o', basefmt='k-', label=f'отсчёты, fs = {fs} Гц')
plt.title('Корректная дискретизация: fs > 2*f0')
plt.xlabel('t, мс'); plt.ylabel('амплитуда')
plt.legend(); plt.grid(alpha=0.3)
plt.savefig(os.path.join(SAVE_DIR, 'task2_ok.png'), dpi=150, bbox_inches='tight')
print(f'Точек на период: fs/f0 = {fs/f0:.1f}')

# ---------- Задание 3 ----------
fs = 100
t_s = np.arange(0, 0.2, 1/fs)
x_s = A * np.sin(2*np.pi*f0*t_s)
plt.figure(figsize=(9, 3))
plt.plot(t_hi*1000, x_hi, color='gray', alpha=0.6, label='"аналоговый" сигнал')
plt.stem(t_s*1000, x_s, linefmt='C0-', markerfmt='C0o', basefmt='k-', label=f'отсчёты, fs = {fs} Гц')
plt.title('Граничный случай: fs = 2*f0 (зависит от фазы!)')
plt.xlabel('t, мс'); plt.ylabel('амплитуда')
plt.legend(); plt.grid(alpha=0.3)
plt.savefig(os.path.join(SAVE_DIR, 'task3_boundary_sin.png'), dpi=150, bbox_inches='tight')

x_s_cos = A * np.cos(2*np.pi*f0*t_s)
plt.figure(figsize=(9, 3))
plt.plot(t_hi*1000, A*np.cos(2*np.pi*f0*t_hi), color='gray', alpha=0.6, label='"аналоговый" сигнал (cos)')
plt.stem(t_s*1000, x_s_cos, linefmt='C1-', markerfmt='C1o', basefmt='k-', label=f'отсчёты, fs = {fs} Гц, φ=π/2')
plt.title('Граничный случай, φ = π/2: отсчёты = ±A')
plt.xlabel('t, мс'); plt.ylabel('амплитуда')
plt.legend(); plt.grid(alpha=0.3)
plt.savefig(os.path.join(SAVE_DIR, 'task3_boundary_cos.png'), dpi=150, bbox_inches='tight')

# ---------- Задание 4 ----------
fs = 80
t_s = np.arange(0, 0.2, 1/fs)
x_s = A * np.sin(2*np.pi*f0*t_s)
f_alias = abs(f0 - fs)
x_alias = A * np.sin(2*np.pi*f_alias*t_hi)
plt.figure(figsize=(9, 3.5))
plt.plot(t_hi*1000, x_hi, color='gray', alpha=0.5, label=f'истинный сигнал, {f0} Гц')
plt.plot(t_hi*1000, x_alias, 'r--', lw=2, label=f'ложный сигнал, {f_alias} Гц')
plt.stem(t_s*1000, x_s, linefmt='C0-', markerfmt='C0o', basefmt='k-', label=f'отсчёты, fs = {fs} Гц')
plt.title(f'Алиасинг: сигнал {f0} Гц маскируется под {f_alias} Гц')
plt.xlabel('t, мс'); plt.ylabel('амплитуда')
plt.legend(); plt.grid(alpha=0.3)
plt.savefig(os.path.join(SAVE_DIR, 'task4_aliasing.png'), dpi=150, bbox_inches='tight')
print(f'fa = |f0 - k*fs| = |{f0} - 1*{fs}| = {f_alias} Гц')

# ---------- Задание 5 ----------
cases = [(500, 'fs = 500 Гц (fs > 2*f0: OK)'),
         (100, 'fs = 100 Гц (fs = 2*f0: граница)'),
         (80,  'fs = 80 Гц (fs < 2*f0: АЛИАСИНГ)')]
fig, ax = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
for a, (fs, ttl) in zip(ax, cases):
    t_s = np.arange(0, 0.2, 1/fs)
    x_s = A * np.sin(2*np.pi*f0*t_s)
    a.plot(t_hi*1000, x_hi, color='gray', alpha=0.5)
    a.stem(t_s*1000, x_s, linefmt='C0-', markerfmt='C0o', basefmt='k-')
    a.set_title(ttl, fontsize=10)
    a.grid(alpha=0.3)
ax[-1].set_xlabel('t, мс')
fig.suptitle(f'Дискретизация синусоиды {f0} Гц с разными fs (вариант 4)', y=0.98)
fig.tight_layout()
fig.savefig(os.path.join(SAVE_DIR, 'task5_three_panels.png'), dpi=150, bbox_inches='tight')

# ---------- Задание 6 ----------
ratios = np.arange(1.1, 3.01, 0.1)
fs_values = ratios * f0
fa_values = []
for fs in fs_values:
    k = round(f0/fs) or 1
    fa = abs(f0 - k*fs)
    while fa > fs/2:
        fa = abs(fa - fs)
    fa_values.append(fa)
plt.figure(figsize=(9, 4))
plt.plot(fs_values, fa_values, 'o-')
plt.axvline(2*f0, color='r', linestyle='--', alpha=0.5, label='fs = 2*f0 (граница Найквиста)')
plt.title(f'Зависимость ложной частоты fa от fs (f0 = {f0} Гц)')
plt.xlabel('fs, Гц'); plt.ylabel('fa, Гц')
plt.legend(); plt.grid(alpha=0.3)
plt.savefig(os.path.join(SAVE_DIR, 'task6_sweep.png'), dpi=150, bbox_inches='tight')

# ---------- Задание 7 (вариант 4) ----------
f0_v = 50
fs_ok, fs_bound, fs_alias = 500, 100, 80
fig, ax = plt.subplots(3, 1, figsize=(9, 7), sharex=True)
cases_v = [(fs_ok, 'OK: fs = 500 Гц'), (fs_bound, 'граница: fs = 100 Гц'), (fs_alias, 'алиасинг: fs = 80 Гц')]
for a, (fs, ttl) in zip(ax, cases_v):
    t_s = np.arange(0, 0.2, 1/fs)
    x_s = A * np.sin(2*np.pi*f0_v*t_s)
    a.plot(t_hi*1000, A*np.sin(2*np.pi*f0_v*t_hi), color='gray', alpha=0.5)
    a.stem(t_s*1000, x_s, linefmt='C0-', markerfmt='C0o', basefmt='k-')
    a.set_title(ttl, fontsize=10)
    a.grid(alpha=0.3)
ax[-1].set_xlabel('t, мс')
fig.suptitle('Задание 7 (вариант 4): f0 = 50 Гц', y=0.98)
fig.tight_layout()
fig.savefig(os.path.join(SAVE_DIR, 'task7_variant4.png'), dpi=150, bbox_inches='tight')
fa_v = abs(f0_v - fs_alias)
print(f'fa = |{f0_v} - {fs_alias}| = {fa_v} Гц')

f1, f2, fs_dop = 50, 130, 80
t_s = np.arange(0, 0.2, 1/fs_dop)
x1_s = A * np.sin(2*np.pi*f1*t_s)
x2_s = A * np.sin(2*np.pi*f2*t_s)
fa1 = abs(f1 - fs_dop)
fa2 = abs(f2 - round(f2/fs_dop)*fs_dop)
print(f'fa(50 Гц)  = {fa1} Гц')
print(f'fa(130 Гц) = {fa2} Гц')
plt.figure(figsize=(9, 4))
plt.plot(t_hi*1000, A*np.sin(2*np.pi*30*t_hi), 'r--', lw=2, label='ложный сигнал, 30 Гц')
plt.stem(t_s*1000, x1_s, linefmt='C0-', markerfmt='C0o', basefmt='k-', label='отсчёты сигнала 50 Гц')
plt.stem(t_s*1000, x2_s, linefmt='C2-', markerfmt='C2x', basefmt='k-', label='отсчёты сигнала 130 Гц')
plt.title('Доп. задание: 50 Гц и 130 Гц при fs = 80 Гц — оба дают fa = 30 Гц')
plt.xlabel('t, мс'); plt.ylabel('амплитуда')
plt.legend(); plt.grid(alpha=0.3)
plt.savefig(os.path.join(SAVE_DIR, 'task7_dop.png'), dpi=150, bbox_inches='tight')