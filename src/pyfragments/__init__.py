from __future__ import annotations

from contextlib import contextmanager

import matplotlib.pyplot as plt
from IPython.display import display
from matplotlib.figure import Figure

_warning_comment = (
    '<!-- You forgot to put "#| output: asis" at the beginning of this code-block.-->'
)


@contextmanager
def animated_figure(fig: Figure, *, add_warning_comment: bool = True):
    if add_warning_comment:
        print(_warning_comment)
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
