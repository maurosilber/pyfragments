from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

import matplotlib.pyplot as plt
from IPython.display import display
from matplotlib.figure import Figure

_warning_comment = (
    '<!-- You forgot to put "#| output: asis" at the beginning of this code-block.-->'
)


class AnimatedFigure:
    def __init__(
        self,
        fig: Figure = None,
        *,
        add_warning_comment: bool = True,
    ):
        self.fig = fig
        self.add_warning_comment = add_warning_comment

    def __enter__(self) -> Self:
        if self.add_warning_comment:
            print(_warning_comment)
        print("::: {.r-stack}")
        return self

    def __exit__(self, *args):
        print(":::")
        plt.close(self.fig)

    @contextmanager
    def fragment(self):
        print("::: {.fragment}")
        yield
        display(self.fig)
        print(":::")
