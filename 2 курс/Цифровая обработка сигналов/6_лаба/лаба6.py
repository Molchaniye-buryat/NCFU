import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy.signal import medfilt, get_window, spectrogram

rng = np.random.default_rng(42)
FS = 1000.0 # Гц
N = 2000
t = np.arange(N) / FS # с

clean = 0.5 * np.sin(2 * np.pi * 1.5 * t) # Гц, с
clean += np.where(t >= 0.8, 1.5, 0.0) # с
clean += np.where((t >= 1.4) & (t < 1.42), 2.0, 0.0) # с

SIGMA = 0.35
noise = rng.normal(0.0, SIGMA, N)
x = clean + noise

def ma_loop(sig, M):
    out = np.zeros_like(sig)
    half = M // 2
    for n in range(sig.size):
        lo = max(0, n - half)
        hi = min(sig.size, n + half + 1)
        out[n] = np.mean(sig[lo:hi])
    return out

def ma_convolve(sig, M, mode="same"):
    kernel = np.ones(M) / M
    return np.convolve(sig, kernel, mode=mode)

def ma_cumsum(sig, M):
    pad = M // 2
    s = np.pad(sig, (pad, M - 1 - pad), mode="edge")
    c = np.cumsum(np.insert(s, 0, 0.0))
    return (c[M:] - c[:-M]) / M

M_TEST = 21
y1 = ma_loop(x, M_TEST)
y2 = ma_convolve(x, M_TEST)
y3 = ma_cumsum(x, M_TEST)
sl = slice(M_TEST, N - M_TEST)
print("max|loop - convolve| =", np.max(np.abs(y1[sl] - y2[sl])))
print("max|cumsum - convolve| =", np.max(np.abs(y3[sl] - y2[sl])))

WINDOWS = [5, 50, 500]
results = {M: ma_convolve(x, M) for M in WINDOWS}
colors = ["tab:blue", "tab:orange", "tab:red"]

# Задания 1-3
fig, ax = plt.subplots(len(WINDOWS) + 1, 1, figsize=(12, 11), sharex=True)
ax[0].plot(t, x, lw=0.5, color="0.6", label="зашумлённый")
ax[0].plot(t, clean, lw=1.4, color="k", label="эталон")
ax[0].set_title("Исходный сигнал")
ax[0].legend(loc="upper right")
ax[0].grid(alpha=0.3)

for i, M in enumerate(WINDOWS):
    ax[i + 1].plot(t, x, lw=0.4, color="0.85")
    ax[i + 1].plot(t, clean, lw=1.0, color="k", alpha=0.5, label="эталон")
    ax[i + 1].plot(t, results[M], lw=1.6, color=colors[i], label=f"SMA, M={M}")
    ax[i + 1].set_title(f"Окно M={M} отсчётов ({1000 * M / FS:.1f} мс), fc ~ {0.443 * FS / M:.2f} Гц")
    ax[i + 1].legend(loc="upper right")
    ax[i + 1].grid(alpha=0.3)

ax[-1].set_xlabel("Время, с")
plt.tight_layout()
plt.savefig("fig1_windows.png", dpi=150)
plt.close()

plt.figure(figsize=(11, 4.5))
m = (t > 0.70) & (t < 1.05) # с
plt.plot(t[m], x[m], lw=0.5, color="0.75", label="шум")
plt.plot(t[m], clean[m], "k", lw=2, label="идеальная ступенька")
for M, c in zip(WINDOWS, colors):
    plt.plot(t[m], results[M][m], lw=1.6, color=c, label=f"M={M}")
plt.title("Размытие фронта при разных размерах окна")
plt.xlabel("Время, с")
plt.ylabel("Амплитуда")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("fig2_step.png", dpi=150)
plt.close()

# Задание 4
def rise_time(sig, fs, t_arr, t_edge=0.8, span=0.3): # Гц, с
    m = (t_arr > t_edge - span) & (t_arr < t_edge + span)
    seg, ts = sig[m], t_arr[m]
    lo, hi = seg[0], seg[-1]
    a, b = lo + 0.1 * (hi - lo), lo + 0.9 * (hi - lo)
    try:
        i10 = np.where(seg >= a)[0][0]
        i90 = np.where(seg >= b)[0][0]
        return ts[i90] - ts[i10] # с
    except IndexError:
        return np.nan

mask_flat = (t > 0.05) & (t < 0.70) # с
sigma_in = np.std((x - clean)[mask_flat])
print(f"{'M':>5} | {'СКО шума':>9} | {'Дисперсия':>9} | {'Выигрыш':>8} | {'sqrt(M)':>8} | {'t_rise, мс':>10} | {'fc, Гц':>8}")
print("-" * 78)
for M in [5, 20, 50, 100, 500]:
    y = ma_convolve(x, M)
    err = np.std((y - clean)[mask_flat])
    var_err = err ** 2
    tr = rise_time(y, FS, t) * 1000 # мс
    print(f"{M:>5} | {err:9.4f} | {var_err:9.4f} | {sigma_in / err:8.2f} | {np.sqrt(M):8.2f} | {tr:10.2f} | {0.443 * FS / M:8.2f}")

# Задания 5-6
def freq_response(h, fs, npts=4096): # Гц
    H = np.fft.rfft(h, n=npts)
    f = np.fft.rfftfreq(npts, d=1.0 / fs) # Гц
    return f, np.abs(H)

plt.figure(figsize=(11, 5))
for M, c in zip(WINDOWS, colors):
    h = np.ones(M) / M
    f, mag = freq_response(h, FS)
    plt.plot(f, 20 * np.log10(mag + 1e-12), color=c, lw=1.4, label=f"M={M} (fc ~ {0.443 * FS / M:.2f} Гц)")
plt.axhline(-3, color="k", ls=":", lw=1, label="уровень -3 дБ")
plt.title("АЧХ фильтра скользящего среднего")
plt.xlabel("Частота, Гц")
plt.ylabel("Коэффициент передачи, дБ")
plt.xlim(0, 200) # Гц
plt.ylim(-60, 5) # дБ
plt.grid(alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("fig3_afc.png", dpi=150)
plt.close()

M_WIN = 31
kernels = {
    "прямоугольное": np.ones(M_WIN) / M_WIN,
    "треугольное": np.bartlett(M_WIN) / np.bartlett(M_WIN).sum(),
    "Ханна": np.hanning(M_WIN) / np.hanning(M_WIN).sum(),
    "Гаусса": get_window(("gaussian", M_WIN / 6), M_WIN) / get_window(("gaussian", M_WIN / 6), M_WIN).sum(),
}

fig, ax = plt.subplots(1, 2, figsize=(13, 4.5))
for name, h in kernels.items():
    ax[0].plot(np.arange(M_WIN) - M_WIN // 2, h, marker="o", ms=3, label=name)
    f, mag = freq_response(h, FS)
    ax[1].plot(f, 20 * np.log10(mag + 1e-12), label=name)
ax[0].set_title(f"Импульсные характеристики, M={M_WIN}")
ax[0].set_xlabel("n")
ax[0].set_ylabel("h[n]")
ax[0].grid(alpha=0.3)
ax[0].legend()

ax[1].set_title("АЧХ оконных ядер")
ax[1].set_xlabel("Частота, Гц")
ax[1].set_ylabel("Уровень, дБ")
ax[1].set_xlim(0, 200) # Гц
ax[1].set_ylim(-80, 5) # дБ
ax[1].grid(alpha=0.3)
ax[1].legend()
plt.tight_layout()
plt.savefig("fig4_kernels.png", dpi=150)
plt.close()

x_sp = x.copy()
idx = rng.choice(N, 25, replace=False)
x_sp[idx] += rng.choice([-4, 4], 25)

plt.figure(figsize=(12, 5))
plt.plot(t, x_sp, lw=0.4, color="0.8", label="с выбросами")
plt.plot(t, np.convolve(x_sp, kernels["прямоугольное"], "same"), lw=1.4, label="SMA (выбросы размазаны)")
plt.plot(t, medfilt(x_sp, kernel_size=M_WIN), lw=1.4, label="медианный (выбросы удалены)")
plt.plot(t, clean, "k", lw=1.0, alpha=0.6, label="эталон")
plt.title("Линейное усреднение против медианного фильтра")
plt.xlabel("Время, с")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("fig5_median.png", dpi=150)
plt.close()

audio_in = "voice_var4.wav"
if os.path.exists(audio_in):
    fs_a, data_a = wavfile.read(audio_in) # Гц
    x_a = data_a.astype(np.float64) / 32768.0 if data_a.dtype == np.int16 else data_a.astype(np.float64)
    if x_a.ndim > 1:
        x_a = x_a.mean(axis=1)
    fig, ax = plt.subplots(len(WINDOWS), 1, figsize=(11, 9), sharex=True)
    for i, M in enumerate(WINDOWS):
        y_a = ma_convolve(x_a, M)
        peak_a = np.max(np.abs(y_a))
        y_a_save = y_a / peak_a * 0.95 if peak_a > 1.0 else y_a
        wavfile.write(f"voice_sma_M{M}.wav", fs_a, (y_a_save * 32767).astype(np.int16))
        f_s, t_s, S_a = spectrogram(y_a, fs=fs_a, window="hann", nperseg=1024, noverlap=768) # Гц, с
        ax[i].pcolormesh(t_s, f_s, 10 * np.log10(S_a + 1e-12), shading="gouraud", cmap="magma")
        ax[i].set_title(f"Спектрограмма голоса после SMA, M={M}")
        ax[i].set_ylabel("Частота, Гц")
        ax[i].set_ylim(0, fs_a / 2) # Гц
    ax[-1].set_xlabel("Время, с")
    plt.tight_layout()
    plt.savefig("fig6_voice_sma.png", dpi=150)
    plt.close()