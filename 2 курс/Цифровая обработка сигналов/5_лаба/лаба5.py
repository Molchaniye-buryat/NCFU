import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import spectrogram

EPS = 1e-12
IN_FILE = "voice_var4.wav"
OUT_FILE = "voice_var4_filtered.wav"

def make_test_wav(path, fs=22050, dur=4.0): # Гц, с
    t = np.arange(int(fs * dur)) / fs # с
    f0 = 135.0 + 25.0 * np.sin(2 * np.pi * 0.5 * t) # Гц
    phase = 2 * np.pi * np.cumsum(f0 / fs)
    voice = np.zeros_like(t)
    for h, amp in enumerate([1.0, 0.55, 0.35, 0.2, 0.12], start=1):
        voice += amp * np.sin(h * phase)
    env = 0.5 * (1.0 + np.sin(2 * np.pi * 1.8 * t)) ** 2
    voice *= env

    rng = np.random.default_rng(4)
    noise = rng.standard_normal(t.size)
    spec = np.fft.rfft(noise)
    freq = np.fft.rfftfreq(t.size, 1.0 / fs) # Гц
    spec[freq < 6000.0] = 0.0
    hiss = np.fft.irfft(spec, n=t.size)
    hiss /= np.max(np.abs(hiss)) + EPS

    hum = (
        0.06 * np.sin(2 * np.pi * 50.0 * t)
        + 0.04 * np.sin(2 * np.pi * 100.0 * t)
        + 0.03 * np.sin(2 * np.pi * 150.0 * t)
        + 0.02 * np.sin(2 * np.pi * 200.0 * t)
    )

    sig = 0.8 * voice / (np.max(np.abs(voice)) + EPS) + 0.25 * hiss + hum
    sig /= np.max(np.abs(sig)) + EPS
    wavfile.write(path, fs, (sig * 32767).astype(np.int16))

def load_wav(path):
    fs, data = wavfile.read(path) # Гц
    if data.dtype == np.int16:
        x = data.astype(np.float64) / 32768.0
    elif data.dtype == np.int32:
        x = data.astype(np.float64) / 2147483648.0
    elif data.dtype == np.uint8:
        x = (data.astype(np.float64) - 128.0) / 128.0
    else:
        x = data.astype(np.float64)
    if x.ndim > 1:
        x = x.mean(axis=1)
    x = x - np.mean(x)
    return fs, x

def make_mask_var4(freqs, notch_half_bw=2.0, f_lowpass=6000.0, trans=300.0): # Гц
    H = np.ones_like(freqs, dtype=np.float64)
    for f0 in (50.0, 100.0, 150.0, 200.0): # Гц
        H[np.abs(freqs - f0) <= notch_half_bw] = 0.0
    if trans > 0:
        a = f_lowpass - trans / 2.0 # Гц
        b = f_lowpass + trans / 2.0 # Гц
        idx_mid = (freqs > a) & (freqs < b)
        y_mid = (freqs[idx_mid] - a) / (b - a)
        H[idx_mid] *= 0.5 * (1.0 + np.cos(np.pi * y_mid))
    H[freqs >= b] = 0.0
    return H

# Задания 1-3
if not os.path.exists(IN_FILE):
    make_test_wav(IN_FILE)

fs, x = load_wav(IN_FILE) # Гц
N = x.size
t = np.arange(N) / fs # с

print(f"Частота дискретизации: {fs} Гц")
print(f"Число отсчётов: {N}")
print(f"Длительность: {N / fs:.2f} с")
print(f"Частота Найквиста: {fs / 2:.1f} Гц")

X = np.fft.rfft(x)
freqs = np.fft.rfftfreq(N, d=1.0 / fs) # Гц
A = np.abs(X) / N
A_db = 20 * np.log10(A + EPS) # дБ

fig, ax = plt.subplots(2, 1, figsize=(11, 7))
ax[0].plot(t, x, lw=0.4)
ax[0].set_title("Осциллограмма исходного сигнала")
ax[0].set_xlabel("Время, с")
ax[0].set_ylabel("Амплитуда")
ax[0].grid(alpha=0.3)

ax[1].semilogx(freqs[1:], A_db[1:], lw=0.6)
ax[1].set_title("Амплитудный спектр всего сигнала")
ax[1].set_xlabel("Частота, Гц")
ax[1].set_ylabel("Уровень, дБ")
ax[1].set_xlim(20, fs / 2)
ax[1].grid(alpha=0.3, which="both")

plt.tight_layout()
plt.savefig("fig1_time_spectrum.png", dpi=150)
plt.close()

# Задания 4-5
NPERSEG = 4096
NOVERLAP = 3072

f_sp, t_sp, Sxx = spectrogram(
    x,
    fs=fs,
    window="hann",
    nperseg=NPERSEG,
    noverlap=NOVERLAP,
    scaling="spectrum",
    mode="psd",
) # Гц, с
Sxx_db = 10 * np.log10(Sxx + EPS) # дБ

P_mean = Sxx.mean(axis=1)
P_db = 10 * np.log10(P_mean + EPS) # дБ
cum = np.cumsum(P_mean) / np.sum(P_mean)
f_low = f_sp[np.searchsorted(cum, 0.025)] # Гц
f_high = f_sp[np.searchsorted(cum, 0.975)] # Гц
f_peak = f_sp[np.argmax(P_mean)] # Гц

print(f"Разрешение по частоте (nperseg={NPERSEG}): {fs / NPERSEG:.2f} Гц")
print(f"Пик средней мощности: {f_peak:.1f} Гц")
print(f"Полоса 95 % энергии: {f_low:.0f} - {f_high:.0f} Гц")

plt.figure(figsize=(11, 4.5))
plt.pcolormesh(t_sp, f_sp, Sxx_db, shading="gouraud", cmap="magma")
plt.colorbar(label="Уровень, дБ")
plt.title(f"Спектрограмма исходного сигнала (Ханна, nperseg={NPERSEG}, df={fs / NPERSEG:.1f} Гц)")
plt.xlabel("Время, с")
plt.ylabel("Частота, Гц")
plt.ylim(0, fs / 2)
plt.tight_layout()
plt.savefig("fig2_spectrogram_before.png", dpi=150)
plt.close()

plt.figure(figsize=(10, 4))
plt.semilogx(f_sp[1:], P_db[1:])
plt.axvline(f_low, color="g", ls="--", label=f"{f_low:.0f} Гц")
plt.axvline(f_high, color="r", ls="--", label=f"{f_high:.0f} Гц")
plt.title("Усреднённый спектр мощности")
plt.xlabel("Частота, Гц")
plt.ylabel("Уровень, дБ")
plt.grid(alpha=0.3, which="both")
plt.legend()
plt.tight_layout()
plt.savefig("fig3_mean_psd.png", dpi=150)
plt.close()

# Задания 6-7
F_CUT = 6000.0 # Гц
TRANS = 300.0 # Гц
NOTCH_BW = 2.0 # Гц

H = make_mask_var4(freqs, notch_half_bw=NOTCH_BW, f_lowpass=F_CUT, trans=TRANS)
Y = H * X
y = np.real(np.fft.irfft(Y, n=N))

plt.figure(figsize=(10, 3.5))
plt.plot(freqs, H)
plt.title(f"Передаточная функция фильтра (fc={F_CUT:.0f} Гц, переход {TRANS:.0f} Гц)")
plt.xlabel("Частота, Гц")
plt.ylabel("H(f)")
plt.xlim(0, fs / 2)
plt.ylim(-0.05, 1.1)
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("fig4_mask.png", dpi=150)
plt.close()

peak = np.max(np.abs(y))
y_out = y / peak * 0.95 if peak > 1.0 else y
wavfile.write(OUT_FILE, fs, (y_out * 32767).astype(np.int16))
print(f"Результат сохранён в {OUT_FILE}")

# ===== ЗАДАЧА 8. Сравнение спектрограмм и оценка энергии =====
f2, t2, Syy = spectrogram(
    y,
    fs=fs,
    window="hann",
    nperseg=NPERSEG,
    noverlap=NOVERLAP,
    scaling="spectrum",
    mode="psd",
) # Гц, с
Syy_db = 10 * np.log10(Syy + EPS) # дБ

vmin = max(Sxx_db.max() - 80, Sxx_db.min()) # дБ
vmax = Sxx_db.max() # дБ

fig, ax = plt.subplots(2, 1, figsize=(11, 8), sharex=True)
im0 = ax[0].pcolormesh(t_sp, f_sp, Sxx_db, shading="gouraud", cmap="magma", vmin=vmin, vmax=vmax)
ax[0].set_title("ДО фильтрации")
ax[0].set_ylabel("Частота, Гц")
fig.colorbar(im0, ax=ax[0], label="дБ")

im1 = ax[1].pcolormesh(t2, f2, Syy_db, shading="gouraud", cmap="magma", vmin=vmin, vmax=vmax)
ax[1].axhline(F_CUT, color="cyan", ls="--", lw=1)
ax[1].set_title(f"ПОСЛЕ фильтрации (fc = {F_CUT:.0f} Гц)")
ax[1].set_xlabel("Время, с")
ax[1].set_ylabel("Частота, Гц")
fig.colorbar(im1, ax=ax[1], label="дБ")

plt.tight_layout()
plt.savefig("fig5_compare.png", dpi=150)
plt.close()

Ex = np.sum(x ** 2)
Ey = np.sum(y ** 2)
removed_share = 100.0 * (1.0 - Ey / (Ex + EPS)) # %
print(f"Энергия до / после: {Ex:.3f} / {Ey:.3f}")
print(f"Удалено энергии: {removed_share:.2f} %")