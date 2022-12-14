import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm

def plot_vol_smile(strikes: [float], ivs: [float]):
    fig, ax = plt.subplots()
    ax.plot(strikes, ivs, "o-")
    ax.set_xlabel("Strikes", size=12)
    ax.set_ylabel("Vols", size=12)
    fig.tight_layout()
    return fig


def plot_vol_surface(strikes: [float], expiry: [float], ivs: [float]):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    X, Y = np.meshgrid(strikes, expiry)
    Z = np.array(ivs).reshape(len(X), len(X[0]))
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                        linewidth=0.1)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    return fig
