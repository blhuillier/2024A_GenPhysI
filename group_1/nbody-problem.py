import numpy as np
import matplotlib.pyplot as plt


def calc_acceleration(p, m, g, s):
    x = p[:, 0:1]
    y = p[:, 1:2]
    z = p[:, 2:3]

    dx = x.T - x
    dy = y.T - y
    dz = z.T - z

    inv_r3 = dx**2 + dy**2 + dz**2 + s**2
    inv_r3[inv_r3 > 0] = inv_r3[inv_r3 > 0] ** (-1.5)

    ax = g * (dx * inv_r3) @ m
    ay = g * (dy * inv_r3) @ m
    az = g * (dz * inv_r3) @ m

    a = np.hstack((ax, ay, az))

    return a


def calc_energy(p, v, m, g):
    ke = 0.5 * np.sum(np.sum(m * v**2))

    x = p[:, 0:1]
    y = p[:, 1:2]
    z = p[:, 2:3]

    dx = x.T - x
    dy = y.T - y
    dz = z.T - z

    inv_r = np.sqrt(dx**2 + dy**2 + dz**2)
    inv_r[inv_r > 0] = 1.0 / inv_r[inv_r > 0]

    pe = g * np.sum(np.sum(np.triu(-(m * m.T) * inv_r, 1)))

    return ke, pe


def simulation():
    n = 100
    t = 0
    t_end = 10.0
    dt = 0.01
    softening = 0.1
    g = 1.0
    plot_real_time = True

    np.random.seed(17)

    m = 20.0 * np.ones((n, 1)) / n
    p = np.random.randn(n, 3)
    v = np.random.randn(n, 3)

    v -= np.mean(m * v, 0) / np.mean(m)

    a = calc_acceleration(p, m, g, softening)

    ke, pe = calc_energy(p, v, m, g)

    nt = int(np.ceil(t_end / dt))

    pos_save = np.zeros((n, 3, nt + 1))
    pos_save[:, :, 0] = p
    ke_save = np.zeros(nt + 1)
    ke_save[0] = ke
    pe_save = np.zeros(nt + 1)
    pe_save[0] = pe
    t_all = np.arange(nt + 1) * dt

    fig = plt.figure(figsize=(4, 5), dpi=80)
    grid = plt.GridSpec(3, 1, wspace=0.0, hspace=0.3)
    ax1 = plt.subplot(grid[0:2, 0])
    ax2 = plt.subplot(grid[2, 0])

    for i in range(nt):
        v += a * dt / 2.0
        p += v * dt
        a = calc_acceleration(p, m, g, softening)
        v += a * dt / 2.0
        t += dt
        ke, pe = calc_energy(p, v, m, g)
        pos_save[:, :, i + 1] = p
        ke_save[i + 1] = ke
        pe_save[i + 1] = pe

        if plot_real_time or (i == nt - 1):
            plt.sca(ax1)
            plt.cla()
            xx = pos_save[:, 0, max(i - 50, 0) : i + 1]
            yy = pos_save[:, 1, max(i - 50, 0) : i + 1]
            plt.scatter(xx, yy, s=1, color=[0.7, 0.7, 1])
            plt.scatter(p[:, 0], p[:, 1], s=10, color="blue")
            ax1.set(xlim=(-2, 2), ylim=(-2, 2))
            ax1.set_aspect("equal", "box")
            ax1.set_xticks([-2, -1, 0, 1, 2])
            ax1.set_yticks([-2, -1, 0, 1, 2])

            plt.sca(ax2)
            plt.cla()
            plt.scatter(
                t_all, ke_save, color="red", s=1, label="KE" if i == nt - 1 else ""
            )
            plt.scatter(
                t_all, pe_save, color="blue", s=1, label="PE" if i == nt - 1 else ""
            )
            plt.scatter(
                t_all,
                ke_save + pe_save,
                color="black",
                s=1,
                label="Etot" if i == nt - 1 else "",
            )
            ax2.set(xlim=(0, t_end), ylim=(-300, 300))
            ax2.set_aspect(0.007)
            plt.pause(0.001)

    plt.sca(ax2)
    plt.xlabel("time")
    plt.ylabel("energy")
    ax2.legend(loc="upper right")

    plt.savefig("nbody.png", dpi=240)
    plt.show()

    return 0


simulation()
