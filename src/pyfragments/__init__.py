from __future__ import annotations

from contextlib import contextmanager
from io import BytesIO
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Self

    from numpy import bool_
    from numpy.typing import NDArray

import imageio as imageio
import matplotlib.pyplot as plt
from IPython.display import Image, Markdown, display
from matplotlib.figure import Figure
from matplotlib.transforms import Bbox

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

    For debugging the presentation, check out `AnimatedFigure.config`.
    """

    class config:
        """Global config for AniamtedFigures.

        Attributes:
            flatten: bool
                If True, renders only the last figure.
            diff: bool
                If True, renders only the difference in each new fragment.
        """

        flatten: bool = False
        diff: bool = True

    def __init__(
        self,
        fig: Figure | None = None,
        *,
        bbox_inches: Bbox
        | tuple[tuple[float, float], tuple[float, float]]
        | None = None,
        add_warning_comment: bool = True,
    ):
        if fig is None:
            fig = plt.figure()
        if isinstance(bbox_inches, tuple):
            bbox_inches = Bbox(bbox_inches)
        self.fig = fig
        self.bbox_inches = bbox_inches
        self.last_image = None
        self.add_warning_comment = add_warning_comment

    def __enter__(self) -> Self:
        if self.add_warning_comment:
            print(_warning_comment)
        display(Markdown("::: {.r-stack}"))
        return self

    def __exit__(self, *args):
        if self.config.flatten:
            display(self.fig)
        display(Markdown(":::"))
        plt.close(self.fig)

    @contextmanager
    def fragment(self):
        if self.config.flatten:
            yield
            return

        display(Markdown(":::: {.fragment}"))
        yield

        if not self.config.diff:
            display(self.fig)
            display(Markdown("::::"))
            return

        # To save space,
        # compute difference from previous image
        # and output only the difference.
        with BytesIO() as buf:
            self.fig.savefig(buf, format="png", bbox_inches=self.bbox_inches)
            image = imageio.imread(buf)

        diff = _diff(image, self.last_image) if self.last_image is not None else image
        self.last_image = image

        with BytesIO() as buf:
            imageio.imwrite(
                buf,
                diff,
                format="png",  # type: ignore
            )
            display(Image(buf.getvalue()))
        display(Markdown("::::"))


def _erode_inplace(data: NDArray[bool_]) -> NDArray[bool_]:
    data[0] = data[0] & data[1]
    data[-1] = data[-2] & data[-1]
    data[1:-1] = data[2:] & data[1:-1] & data[:-2]
    return data


def _erode2D_inplace(data: NDArray[bool_]) -> NDArray[bool_]:
    _erode_inplace(data)
    _erode_inplace(data.T)
    return data


def _diff(image: NDArray, last_image: NDArray):
    diff = image.copy()
    mask = (image == last_image).all(-1)
    mask = _erode2D_inplace(mask)
    diff[mask] = 0
    return diff
