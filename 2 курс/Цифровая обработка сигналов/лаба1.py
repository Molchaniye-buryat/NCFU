import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import os

#ВАРИАНТ 4

OUT = r"E:\NCFU\2 курс\Цифровая обработка сигналов"
os.makedirs(OUT, exist_ok=True)

fs = 300.0
T = 4.0

t1 = np.arange(0, T, 1/fs)
t2 = np.linspace(0, T, int(T*fs), endpoint = False)

print('Задание 1')
print(len(t1), len(t2))
print()

print('Задание 2')
A, f, phi = 1.2, 2, 0
x_demo = A * np.sin(2*np.pi*f*t1 + phi)

plt.figure(figsize=(9, 3))
plt.plot(t1, x_demo, lw=1.5)
plt.title(f'Harmonic signal : A={A}, f={f} Hz')
plt.xlabel('t, s')
plt.ylabel('x(t)')
plt.grid (alpha = 0.3)
plt.xlim (0 , 1.5)
plt.savefig(f"{OUT}/task2_harmonic.png", dpi=130, bbox_inches="tight")
plt.close()
print()

print('Задание 3')
f0 = 2.0
sq = signal.square(2*np.pi*f0*t1, duty=0.5)
sw = signal.sawtooth(2*np.pi*f0*t1)
rng = np.random.default_rng(42)
wn = rng.normal(0, 0.5, size=t1.shape)

fig, ax = plt.subplots(2, 2, figsize=(10, 5), sharex=True)
ax[0, 0].plot(t1, x_demo); ax[0, 0].set_title("Sine")
ax[0, 1].plot(t1, sq); ax[0, 1].set_title("Square")
ax[1, 0].plot(t1, sw); ax[1, 0].set_title("Sawtooth")
ax[1, 1].plot(t1, wn); ax[1, 1].set_title("White noise")
for a in ax.flat:
	a.set_xlim(0, 1.5); a.grid(alpha=0.3); a.set_xlabel("t, s")
fig.tight_layout()
fig.savefig(f"{OUT}/task3_grid.png", dpi=130)
plt.close(fig)
print()

print('Задание 4')
plt.figure(figsize=(9, 3))
plt.plot(t1, x_demo, label="sine 2 Hz")
plt.plot(t1, sq, "--", label="square 2 Hz")
plt.plot(t1, 0.5*wn, alpha=0.7, label="noise (x0.5)")
plt.title("Several signals on one axes")
plt.xlabel("t, s"); plt.ylabel("amplitude")
plt.legend(loc="upper right")
plt.grid(alpha=0.3)
plt.xlim(0, 1.5)
plt.tight_layout()
plt.savefig(f"{OUT}/task4_combined.png", dpi=130)
plt.close()
print()

print('Задание 5')
f1d, f2d, f3d = 3, 8, 15
A1d, A2d, A3d = 1.0, 0.6, 0.3
s1 = A1d*np.sin(2*np.pi*f1d*t1)
s2 = A2d*np.sin(2*np.pi*f2d*t1)
s3 = A3d*np.sin(2*np.pi*f3d*t1)
s_demo = s1 + s2 + s3

plt.figure(figsize=(9, 3))
plt.plot(t1, s1, "--", alpha=0.6, label=f"{f1d} Hz")
plt.plot(t1, s2, "--", alpha=0.6, label=f"{f2d} Hz")
plt.plot(t1, s3, "--", alpha=0.6, label=f"{f3d} Hz")
plt.plot(t1, s_demo, "k", lw=1.8, label="sum")
plt.title("Sum of three sinusoids (demo)")
plt.xlabel("t, s"); plt.ylabel("amplitude")
plt.legend(ncol=4); plt.grid(alpha=0.3)
plt.xlim(0, 1.0)
plt.tight_layout()
plt.savefig(f"{OUT}/task5_sum_demo.png", dpi=130)
plt.close()
print()

print('Задание 6')
f1, f2, f3 = 2, 8, 20
A1, A2, A3 = 1.2, 0.4, 0.2
phi1, phi2, phi3 = 0, np.pi/2, np.pi

s1 = A1*np.sin(2*np.pi*f1*t1 + phi1)
s2 = A2*np.sin(2*np.pi*f2*t1 + phi2)
s3 = A3*np.sin(2*np.pi*f3*t1 + phi3)
s = s1 + s2 + s3

plt.figure(figsize=(9, 3.2))
plt.plot(t1, s1, "--", alpha=0.6, label=f"{f1} Hz")
plt.plot(t1, s2, "--", alpha=0.6, label=f"{f2} Hz")
plt.plot(t1, s3, "--", alpha=0.6, label=f"{f3} Hz")
plt.plot(t1, s, "k", lw=1.8, label="sum")
plt.title("Вариант 4: сумма трёх синусоид (2, 8, 20 Гц)")
plt.xlabel("t, s"); plt.ylabel("амплитуда")
plt.legend(ncol=4); plt.grid(alpha=0.3)
plt.xlim(0, 2.0)
plt.tight_layout()
plt.savefig(f"{OUT}/task6_variant4_sum.png", dpi=130)
plt.close()
print()