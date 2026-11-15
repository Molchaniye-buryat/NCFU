import numpy as np
import matplotlib.pyplot as plt

# Исходные данные
N1 = 1.48
N2 = 1.46
N0 = 1.0
A = 0.5
C = 3e8
L = 10000.0


# Расчёт параметров волокна
def fiber_params(n1=N1, n2=N2, n0=N0):
    theta_c = np.degrees(np.arcsin(n2 / n1))
    NA = np.sqrt(n1**2 - n2**2)
    theta_a = np.degrees(np.arcsin(NA / n0))

    return theta_c, NA, theta_a


# Моделирование распространения луча
def trace_ray(y0, theta_deg, x_max=30.0,
              n1=N1, n2=N2, a=A):

    th = np.radians(theta_deg)

    d = np.array([np.cos(th), np.sin(th)])
    p = np.array([0.0, y0])

    pts = [p.copy()]

    while p[0] < x_max:

        if abs(d[1]) < 1e-12:
            pts.append([x_max, p[1]])
            break

        y_wall = a * np.sign(d[1])

        p = p + d * ((y_wall - p[1]) / d[1])
        pts.append(p.copy())

        sin_i = abs(d[0])

        if sin_i <= n2 / n1:
            d[1] = -d[1]

        else:
            phi_t = np.arcsin(min((n1 / n2) * sin_i, 1.0))
            ang = np.pi / 2 - phi_t

            d = np.array([
                np.cos(ang),
                np.sign(y_wall) * np.sin(ang)
            ])

            pts.append(
                p + d * ((x_max - p[0]) / d[0])
            )
            break

    return np.array(pts)


# Задание 1

tc, NA, ta = fiber_params()

theta_max = 90 - tc

print(f"Критический угол: {tc:.2f} град.")
print(f"Максимальный угол внутри: {theta_max:.2f} град.")
print(f"Числовая апертура: {NA:.3f}")
print(f"Апертурный угол: {ta:.2f} град.")


# Задание 2

X_MAX = 30.0

fig, ax = plt.subplots(figsize=(10, 3.6))

ax.fill_between(
    [0, X_MAX], -A, A,
    color="lightblue",
    alpha=0.35
)

ax.axhline(A, color="gray")
ax.axhline(-A, color="gray")

for th in [3, 8, 13, 18, 25]:

    pts = trace_ray(0.0, th, X_MAX)

    guided = np.cos(np.radians(th)) >= N2 / N1

    ax.plot(
        pts[:, 0],
        pts[:, 1],
        lw=2,
        label=f"{th} град. ({'направляемый' if guided else 'вытекающий'})"
    )

ax.set_ylim(-2.2, 2.2)
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title("Траектории лучей в оптическом волокне")
ax.legend(loc="upper right", fontsize=8)

plt.savefig("trajectories.png", dpi=300, bbox_inches="tight")
plt.close()


# Задание 3

angles = np.linspace(0.1, 30.0, 3000)

guided = np.cos(np.radians(angles)) >= N2 / N1

theta_max_num = angles[guided].max()

theta_a_num = np.degrees(
    np.arcsin(
        N1 * np.sin(np.radians(theta_max_num)) / N0
    )
)

print(f"Максимальный угол внутри: {theta_max_num:.2f} град.")
print(f"Теоретический угол: {theta_max:.2f} град.")
print(f"Численный апертурный угол: {theta_a_num:.2f} град.")
print(f"Теоретический апертурный угол: {ta:.2f} град.")


# Задание 4

theta_max_rad = np.radians(theta_max)

t0 = L * N1 / C
t_max = L * N1 / (C * np.cos(theta_max_rad))

dt = t_max - t0

bandwidth = 1 / (2 * dt)

print(f"Время осевого луча: {t0 * 1e6:.3f} мкс")
print(f"Время крайнего луча: {t_max * 1e6:.3f} мкс")
print(f"Межмодовая дисперсия: {dt * 1e9:.2f} нс")
print(f"Пропускная способность: {bandwidth / 1e6:.3f} МГц")


angles = np.linspace(0, theta_max, 20000)

times = L * N1 / (
    C * np.cos(np.radians(angles))
)

plt.figure(figsize=(7, 3.6))

plt.hist(times * 1e6, bins=60)

plt.xlabel("Время прихода, мкс")
plt.ylabel("Количество лучей")
plt.title("Межмодовая дисперсия, L = 10 км")

plt.savefig("dispersion.png", dpi=300, bbox_inches="tight")
plt.close()


# Задание 5

delta = (N1 - N2) / N1

dt = L * N1 / C * (N1 / N2 - 1)

B = 1 / (2 * dt)

print(f"Длина линии: {L / 1000:.0f} км")
print(f"Разность показателей преломления: {delta:.5f}")
print(f"Межмодовая дисперсия: {dt * 1e9:.2f} нс")
print(f"Максимальная оценочная скорость: {B / 1e6:.3f} Мбит/с")