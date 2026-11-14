import numpy as np
import matplotlib.pyplot as plt

# Задание 1
Nx = 500          # количество точек по пространству
dx = 1.0          # шаг по пространству
v = 1.0           # скорость волны
Courant = 0.9     # число Куранта (<= 1)
dt = Courant * dx / v
Nt = 600          # количество шагов по времени
gamma = 0.02      # коэффициент затухания (вариант 4)
save_steps = [0, 50, 100, 200]   # шаги, для которых сохраняются кадры
probe_x = 250     # координата датчика

x = np.arange(Nx) * dx
u_prev = np.zeros(Nx)
u_curr = np.zeros(Nx)
u_next = np.zeros(Nx)
v_arr = np.ones(Nx) * v
K = (v_arr * dt / dx)**2

x0 = 100
width = 15
u_curr = np.exp(-0.5 * ((x - x0) / width)**2)
u_prev = u_curr.copy()

probe_idx = int(probe_x / dx)
probe_data = []
max_amp = []
front_amp = []

# Задание 2
for n in range(Nt):
    u_next[1:-1] = (2*u_curr[1:-1] - u_prev[1:-1]*(1 - gamma*dt) +
                    K[1:-1] * (u_curr[2:] - 2*u_curr[1:-1] + u_curr[:-2])) / (1 + gamma*dt)

    u_next[0] = u_curr[1]
    u_next[-1] = u_curr[-2]

    u_prev[:] = u_curr
    u_curr[:] = u_next

    probe_data.append(u_curr[probe_idx])
    max_amp.append(np.max(np.abs(u_curr)))
    x_front = x0 + v * (n + 1) * dt
    win = (x >= x_front - 40) & (x <= x_front + 40)
    front_amp.append(np.max(u_curr[win]) if win.any() else np.nan)

    if n in save_steps:
        plt.figure(figsize=(9, 4))
        plt.plot(x, u_curr, lw=2, color='red')
        plt.axvline(probe_x, color='green', ls=':', label='Датчик')
        plt.xlim(0, Nx*dx); plt.ylim(-1.2, 1.2)
        plt.xlabel('Координата x'); plt.ylabel('u(x,t)')
        plt.title(f'Шаг времени: {n}')
        plt.legend(); plt.grid(alpha=0.3); plt.tight_layout()
        plt.savefig(f'frame_step_{n}.png', dpi=200); plt.close()

t = np.arange(Nt) * dt
probe_data = np.array(probe_data)
max_amp = np.array(max_amp)
front_amp = np.array(front_amp)

# Задание 3
plt.figure(figsize=(9, 3))
plt.plot(t, probe_data, color='blue')
plt.title(f'Сигнал на датчике (x={probe_x})')
plt.xlabel('Время'); plt.ylabel('Амплитуда u')
plt.grid(alpha=0.3); plt.tight_layout()
plt.savefig('probe_signal.png', dpi=200); plt.close()

# Задание 4
i1, i2 = 60, 420
slope, intercept = np.polyfit(t[i1:i2], np.log(front_amp[i1:i2]), 1)
theory = 0.5 * np.exp(-gamma * t / 2)

print(f"Показатель затухания фронта (подгонка): {slope:.4f} 1/ед.вр.")
print(f"Теоретический показатель -gamma/2:       {-gamma/2:.4f} 1/ед.вр.")
print(f"Время убывания амплитуды фронта в e раз: {-1/slope:.1f} (теория {2/gamma:.1f})")
print(f"Макс. амплитуда по области: старт {max_amp[0]:.3f}, шаг 130: {max_amp[130]:.3f}, шаг 599: {max_amp[-1]:.3f}")
print(f"Макс. |u| на датчике: {np.max(np.abs(probe_data)):.4f}")

plt.figure(figsize=(9, 4))
plt.semilogy(t, max_amp, lw=2, label='max|u| по всей области')
plt.semilogy(t[:i2], front_amp[:i2], lw=2, label='амплитуда фронта (бегущий импульс)')
plt.semilogy(t, theory, 'k--', label=r'теория $0.5\,e^{-\gamma t/2}$')
plt.xlabel('Время'); plt.ylabel('Амплитуда (лог. масштаб)')
plt.title('Затухание волны в среде с потерями')
plt.grid(alpha=0.3, which='both'); plt.legend(); plt.tight_layout()
plt.savefig('max_amplitude.png', dpi=200); plt.close()