from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

import matplotlib.pyplot as plt
from IPython.display import Markdown, display
from matplotlib.figure import Figure

_warning_comment = (
    '<!-- You forgot to put "#| output: asis" at the beginning of this code-block.-->'
)


class AnimatedFigure:
    """Accepts or creates a matplotlib figure,
    and outputs Markdown code to display the figure in fragments.

    Must be used with "output: asis" in Quarto's code-block:

    ```{python}
    #| output: asis
    with AnimatedFigure() as ani:
        for i in range(2):
            with ani.fragment():
                plt.scatter(i, i)
    ```
    """

    def __init__(
        self,
        fig: Figure | None = None,
        *,
        add_warning_comment: bool = True,
        **fig_kw,
    ):
        if fig is None:
            fig = plt.figure(**fig_kw)
        self.fig = fig
        self.add_warning_comment = add_warning_comment

    def __enter__(self) -> Self:
        if self.add_warning_comment:
            print(_warning_comment)
        display(Markdown("::: {.r-stack}"))
        return self

    def __exit__(self, *args):
        display(Markdown(":::"))
        plt.close(self.fig)

    @contextmanager
    def fragment(self):
        display(Markdown(":::: {.fragment}"))
        yield
        display(self.fig)
        display(Markdown("::::"))
