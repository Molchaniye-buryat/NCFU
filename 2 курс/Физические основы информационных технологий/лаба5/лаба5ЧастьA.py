import math
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(2026)

PW50 = 30e-9                                # с, ширина импульса на уровне 0.5
VP = 1.0                                    # мВ, амплитуда одиночного импульса
D_LIST = [0.6, 1.0, 1.5, 2.0, 3.0, 4.0]     # набор плотностей D
D_EYE = [1.0, 2.5, 4.0]                     # плотности для глаз-диаграмм
NBITS = 2000                                # длина битовой последовательности
NBITS_BER = 200000                          # длина последовательности для Монте-Карло BER
SNR_DB = 24.0                               # отношение сигнал/шум, дБ
SPS = 32                                    # отсчётов на битовый интервал
BER_LIMIT = 1e-4                            # допустимая вероятность ошибки
N_TAPS = 21                                 # число отводов эквалайзера PR4

erfc_v = np.vectorize(math.erfc)

def q_func(x):
    return 0.5 * erfc_v(np.asarray(x) / math.sqrt(2.0))

def lorentz(t, pw50=PW50, vp=VP):
    return vp / (1.0 + (2.0 * t / pw50) ** 2)

def dibit(t, T, pw50=PW50, vp=VP):
    return lorentz(t, pw50, vp) - lorentz(t - T, pw50, vp)

def nrzi_transitions(bits):
    c = np.zeros(len(bits))
    pol = 1
    for k, b in enumerate(bits):
        if b:
            c[k] = pol
            pol = -pol
    return c

def readback_signal(bits, T, sps=SPS, pw50=PW50, vp=VP):
    c = nrzi_transitions(bits)
    dt = T / sps
    stream = np.zeros(len(bits) * sps)
    stream[::sps] = c
    L = int(np.ceil(8 * pw50 / dt))
    th = np.arange(-L, L + 1) * dt
    h = lorentz(th, pw50, vp)
    s = np.convolve(stream, h, mode='same')
    t = np.arange(len(s)) * dt
    return t, s, c

def sampled_signal(c, D):
    M = int(np.ceil(8 * D))
    m = np.arange(-M, M + 1)
    return np.convolve(c, lorentz(m * (PW50 / D)), mode='same')

def amplitude_loss_and_shift(D, pw50=PW50, vp=VP):
    T = pw50 / D
    tt = np.linspace(-3 * pw50, 3 * pw50, 200001)
    d = dibit(tt, T, pw50, vp)
    i = np.argmax(d)
    apk = d[i]
    return apk, 1.0 - apk / vp, tt[i] / T

def eye_diagram(s, sps, n_traces=400, offset=0):
    seg = []
    start = offset + 5 * sps
    for i in range(n_traces):
        a = start + i * sps
        b = a + 2 * sps
        if b < len(s):
            seg.append(s[a:b])
    return np.array(seg)

def eye_opening(s, sps, c):
    k = np.arange(5, len(c) - 5)
    samp = np.abs(s[k * sps])
    on = samp[c[k] != 0]
    off = samp[c[k] == 0]
    return on.min() - (off.max() if len(off) else 0.0)

def simulate_ber(D, snr_db, nbits=NBITS_BER):
    bits = np.random.randint(0, 2, nbits)
    c = nrzi_transitions(bits)
    sigma = VP / (10 ** (snr_db / 20.0))
    samp = sampled_signal(c, D) + np.random.normal(0, sigma, nbits)
    apk, _, _ = amplitude_loss_and_shift(D)
    thr = 0.5 * apk
    det = np.zeros_like(c)
    det[samp > thr] = 1
    det[samp < -thr] = -1
    ber = np.mean(det[5:-5] != c[5:-5])
    ber_th = 2 * float(q_func(thr / sigma))
    return ber, ber_th, sigma

def pr4_taps(D, snr_db=SNR_DB, ntaps=N_TAPS, ntrain=40000):
    c = nrzi_transitions(np.random.randint(0, 2, ntrain))
    sigma = VP / (10 ** (snr_db / 20.0))
    x = sampled_signal(c, D) + np.random.normal(0, sigma, ntrain)
    y = c + np.concatenate(([0.0], c[:-1]))
    L = ntaps // 2
    X = np.column_stack([np.roll(x, m) for m in range(-L, L + 1)])
    w = np.linalg.lstsq(X[L:-L], y[L:-L], rcond=None)[0]
    return w

def apply_taps(s, w, sps=SPS):
    L = len(w) // 2
    g = np.zeros(2 * L * sps + 1)
    g[np.arange(-L, L + 1) * sps + L * sps] = w
    return np.convolve(s, g, mode='same')

# Задание 1
tt = np.linspace(-4 * PW50, 6 * PW50, 4000)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
ax[0].plot(tt * 1e9, lorentz(tt), 'b', lw=2)
ax[0].axhline(VP / 2, color='r', ls='--', lw=1)
ax[0].annotate('', xy=(-PW50 / 2 * 1e9, VP / 2), xytext=(PW50 / 2 * 1e9, VP / 2),
               arrowprops=dict(arrowstyle='<->', color='r'))
ax[0].text(0, VP / 2 + 0.05, 'PW50', color='r', ha='center')
ax[0].set_title('Одиночный лоренцев импульс')
ax[0].set_xlabel('t, нс'); ax[0].set_ylabel('V, мВ'); ax[0].grid(True)
for D in [0.6, 1.0, 2.0, 4.0]:
    ax[1].plot(tt * 1e9, dibit(tt, PW50 / D), lw=1.6, label=f'D={D}')
ax[1].set_title('Дибит-отклик при разной плотности')
ax[1].set_xlabel('t, нс'); ax[1].set_ylabel('V, мВ')
ax[1].legend(); ax[1].grid(True)
plt.tight_layout(); plt.savefig('a1_pulses.png', dpi=200); plt.close()

# Задание 2
bits = np.random.randint(0, 2, 40)
fig, axs = plt.subplots(len(D_LIST), 1, figsize=(11, 12))
for i, D in enumerate(D_LIST):
    T = PW50 / D
    t, s, c = readback_signal(bits, T)
    axs[i].plot(t / T, s, 'b', lw=1.4)
    axs[i].stem(np.arange(len(c)), c * 0.25 * VP, linefmt='r-', markerfmt='ro', basefmt=' ')
    axs[i].set_ylabel(f'D={D}')
    axs[i].grid(True)
axs[-1].set_xlabel('t / T')
plt.suptitle('Сигнал считывания (красное - переходы NRZI)')
plt.tight_layout(); plt.savefig('a2_signals.png', dpi=200); plt.close()

# Задание 3
Ds = np.linspace(0.4, 4.5, 80)
amps, losses, shifts = [], [], []
for D in Ds:
    a, l, sh = amplitude_loss_and_shift(D)
    amps.append(a); losses.append(l * 100); shifts.append(abs(sh))
print(f"{'D':>5} {'T, нс':>7} {'A_pk, мВ':>9} {'потеря, %':>10} {'|сдвиг|, T':>11}")
for D in D_LIST:
    a, l, sh = amplitude_loss_and_shift(D)
    print(f"{D:5.1f} {PW50/D*1e9:7.1f} {a:9.3f} {l*100:10.1f} {abs(sh):11.3f}")

fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
ax[0].plot(Ds, losses, 'b', lw=2)
ax[0].set_xlabel('D = PW50/T'); ax[0].set_ylabel('Потеря амплитуды, %')
ax[0].set_title('Потеря амплитуды'); ax[0].grid(True)
ax[1].plot(Ds, shifts, 'g', lw=2)
ax[1].set_xlabel('D = PW50/T'); ax[1].set_ylabel(r'$|\Delta t_{peak}|/T$')
ax[1].set_title('Сдвиг пика (bit shift)'); ax[1].grid(True)
plt.tight_layout(); plt.savefig('a3_loss.png', dpi=200); plt.close()

# Задание 4
bits = np.random.randint(0, 2, NBITS)
sigma = VP / (10 ** (SNR_DB / 20.0))
fig, axs = plt.subplots(1, len(D_EYE), figsize=(14, 4.2))
print(f"\nsigma = {sigma:.4f} мВ")
print(f"{'D':>5} {'A_eye, мВ':>10} {'Pe = Q(A/2sigma)':>18}")
for j, D in enumerate(D_EYE):
    T = PW50 / D
    t, s, c = readback_signal(bits, T)
    a_eye = eye_opening(s, SPS, c)
    pe = float(q_func(a_eye / (2 * sigma))) if a_eye > 0 else 0.5
    print(f"{D:5.1f} {a_eye:10.3f} {pe:18.2e}")
    s_n = s + np.random.normal(0, sigma, len(s))
    eye = eye_diagram(s_n, SPS)
    x = np.linspace(-1, 1, 2 * SPS)
    for tr in eye:
        axs[j].plot(x, tr, 'b', alpha=0.05, lw=0.8)
    axs[j].set_title(f'Глаз-диаграмма, D={D}')
    axs[j].set_xlabel('t / T'); axs[j].grid(True)
axs[0].set_ylabel('V, мВ')
plt.tight_layout(); plt.savefig('a4_eye.png', dpi=200); plt.close()

# Задание 5
print(f"\n{'D':>5} {'BER (Монте-Карло)':>18} {'BER (теория)':>14}")
Dber, ber_mc, ber_t = [], [], []
for D in np.arange(0.6, 4.01, 0.2):
    b, bt, sg = simulate_ber(D, SNR_DB)
    Dber.append(D); ber_mc.append(max(b, 1e-7)); ber_t.append(max(bt, 1e-12))
    print(f"{D:5.2f} {b:18.2e} {bt:14.2e}")

plt.figure(figsize=(7, 5))
plt.semilogy(Dber, ber_mc, 'bo-', label='Монте-Карло')
plt.semilogy(Dber, ber_t, 'r--', label='теория')
plt.axhline(BER_LIMIT, color='k', ls=':', label=r'$BER=10^{-4}$')
plt.xlabel('D = PW50/T'); plt.ylabel('BER')
plt.title(f'Достоверность канала, SNR = {SNR_DB} дБ')
plt.legend(); plt.grid(True, which='both')
plt.tight_layout(); plt.savefig('a5_ber.png', dpi=200); plt.close()

# Задание 6
Dfine = np.linspace(0.3, 4.5, 400)
ber_theory = np.array([2 * float(q_func(0.5 * amplitude_loss_and_shift(D)[0] / sigma)) for D in Dfine])
Dmax_th = Dfine[ber_theory <= BER_LIMIT].max()
Dber_a = np.array(Dber); ber_mc_a = np.array(ber_mc)
mono = ber_mc_a <= 0.3
Dmax_mc = np.interp(np.log10(BER_LIMIT), np.log10(ber_mc_a[mono]), Dber_a[mono])
print(f"\nD_max по теоретической оценке (без ISI): {Dmax_th:.2f}")
print(f"D_max по Монте-Карло (с учётом ISI):     {Dmax_mc:.2f}")

# Задание 7
D_PR = 2.5
T = PW50 / D_PR
w = pr4_taps(D_PR)
t, s, c = readback_signal(bits, T)
z = apply_taps(s, w)
y = c + np.concatenate(([0.0], c[:-1]))
k = np.arange(15, len(c) - 15)
err = np.max(np.abs(z[k * SPS] - y[k]))
a_eye_pr4 = VP * (1 - 2 * err)
a_eye_lor = eye_opening(s, SPS, c)
noise_gain = float(np.sqrt(np.sum(w ** 2)))
print(f"\nD = {D_PR}: раскрыв глаза лоренцева канала = {a_eye_lor:.3f} мВ")
print(f"D = {D_PR}: раскрыв глаза после PR4-эквалайзера = {a_eye_pr4:.3f} мВ, усиление шума = {noise_gain:.2f}")

s_n = s + np.random.normal(0, sigma, len(s))
z_n = apply_taps(s_n, w)
fig, ax = plt.subplots(1, 2, figsize=(12, 4.2))
x = np.linspace(-1, 1, 2 * SPS)
for tr in eye_diagram(s_n, SPS, offset=(N_TAPS // 2) * SPS):
    ax[0].plot(x, tr, 'b', alpha=0.05, lw=0.8)
for tr in eye_diagram(z_n, SPS, offset=(N_TAPS // 2) * SPS):
    ax[1].plot(x, tr, 'r', alpha=0.05, lw=0.8)
ax[0].set_title(f'Лоренцев канал, D={D_PR}')
ax[1].set_title(f'После эквалайзера PR4, D={D_PR}')
for a in ax:
    a.set_xlabel('t / T'); a.set_ylabel('V, мВ'); a.grid(True)
plt.tight_layout(); plt.savefig('a6_pr4_eye.png', dpi=200); plt.close()

nb = 200000
c_t = nrzi_transitions(np.random.randint(0, 2, nb))
x_t = sampled_signal(c_t, D_PR) + np.random.normal(0, sigma, nb)
L = N_TAPS // 2
z_t = sum(w[m + L] * np.roll(x_t, m) for m in range(-L, L + 1))
y_t = c_t + np.concatenate(([0.0], c_t[:-1]))
det_pr = np.zeros(nb); det_pr[z_t > 0.5] = 1; det_pr[z_t < -0.5] = -1
ber_pr = np.mean(det_pr[L:-L] != y_t[L:-L])
apk = amplitude_loss_and_shift(D_PR)[0]
det_lor = np.zeros(nb); det_lor[x_t > 0.5 * apk] = 1; det_lor[x_t < -0.5 * apk] = -1
ber_lor = np.mean(det_lor[5:-5] != c_t[5:-5])
print(f"BER лоренцева канала (D={D_PR}, SNR={SNR_DB:.0f} дБ): {ber_lor:.2e}")
print(f"BER после PR4 (посимвольный детектор):           {ber_pr:.2e}")