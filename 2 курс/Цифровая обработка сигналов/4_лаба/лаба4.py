import numpy as np
import matplotlib.pyplot as plt

# Задание 1
fs = 1000.0 # Гц
N = 2048
T = N / fs # с
t = np.arange(N) / fs # с

components = [(37.0, 0.9), (155.0, 0.7), (401.0, 0.45)]

np.random.seed(0)
signal = np.zeros(N)
for f0, A in components:
    signal += A * np.sin(2 * np.pi * f0 * t)

sigma = 0.4
noise = np.random.normal(0.0, sigma, N)
signal_noisy = signal + noise

# Задание 2-4
X = np.fft.fft(signal_noisy)

freqs = np.fft.fftfreq(N, d=1.0 / fs) # Гц
half = N // 2
freqs_half = freqs[:half] # Гц

amp = np.abs(X[:half]) * 2.0 / N
amp[0] = np.abs(X[0]) / N

print(f"Частота дискретизации: {fs} Гц")
print(f"Число отсчётов N: {N}")
print(f"Разрешение df = fs/N: {fs / N:.4f} Гц")
print(f"Частота Найквиста: {fs / 2:.1f} Гц")
print("-" * 46)

# Задание 5
def find_dominant(freqs, amp, alpha=8.0):
    noise_level = np.median(amp)
    threshold = alpha * noise_level
    peaks = []
    for k in range(1, len(amp) - 1):
        if amp[k] > threshold and amp[k] > amp[k - 1] and amp[k] > amp[k + 1]:
            peaks.append((freqs[k], amp[k]))
    peaks.sort(key=lambda p: p[1], reverse=True)
    return peaks, threshold, noise_level

peaks, threshold, noise_level = find_dominant(freqs_half, amp, alpha=8.0)

print(f"Медианный уровень шума: {noise_level:.4f}")
print(f"Порог обнаружения: {threshold:.4f}")
print("-" * 46)
print("Доминирующие частоты:")
print(f"{'№':>3} {'f, Гц':>10} {'A':>10}")
for i, (f, a) in enumerate(peaks, 1):
    print(f"{i:>3} {f:>10.2f} {a:>10.4f}")

# Задание 6
fig, ax = plt.subplots(2, 1, figsize=(10, 7))

ax[0].plot(t[:200], signal_noisy[:200], lw=1.0, label="сигнал + шум")
ax[0].plot(t[:200], signal[:200], lw=1.5, alpha=0.8, label="чистый сигнал")
ax[0].set_xlabel("Время, с")
ax[0].set_ylabel("Амплитуда")
ax[0].set_title("Сигнал во временной области (первые 0,2 с)")
ax[0].grid(True, alpha=0.3)
ax[0].legend()

ax[1].plot(freqs_half, amp, lw=1.0)
ax[1].axhline(threshold, color="r", ls="--", lw=1, label=f"порог {threshold:.3f}")
for f, a in peaks:
    ax[1].annotate(
        f"{f:.1f} Гц\nA={a:.2f}",
        xy=(f, a),
        xytext=(f + 12, a + 0.05),
        fontsize=9,
        arrowprops=dict(arrowstyle="->", lw=0.8),
    )
ax[1].set_xlabel("Частота, Гц")
ax[1].set_ylabel("Амплитуда")
ax[1].set_title("Амплитудный спектр (односторонний, нормированный)")
ax[1].set_xlim(0, fs / 2)
ax[1].grid(True, alpha=0.3)
ax[1].legend()
plt.tight_layout()
plt.savefig("lab4_spectrum.png", dpi=200)