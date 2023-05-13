from __future__ import annotations

from contextlib import contextmanager

import matplotlib.pyplot as plt
from IPython.display import display
from matplotlib.figure import Figure


@contextmanager
def animated_figure(fig: Figure):
    print("::: {.r-stack}")
    yield
    print(":::")
    plt.close(fig)


@contextmanager
def fragment(fig: Figure):
    print("::: {.fragment}")
    yield
    display(fig)
    print(":::")
