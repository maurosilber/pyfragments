from __future__ import annotations

from xml.dom import minidom

import numpy as np
from matplotlib.figure import Figure
from pytest import mark

from ..svg import animate


def subplots():
    fig = Figure()
    ax = fig.add_subplot()
    return fig, ax


def get_dom(fig: Figure):
    svg = animate(fig)
    return minidom.parseString(svg.data)


@mark.parametrize(
    ["gid", "index"],
    [
        (".fragment", None),
        (".fragment-1", "1"),
    ],
)
def test_imshow(gid: str, index: str | None):
    fig, ax = subplots()
    ax.imshow(np.random.rand(5, 5), gid=gid)
    dom = get_dom(fig)

    image, *rest = dom.getElementsByTagName("image")
    assert len(rest) == 0
    assert "fragment" in image.attributes["class"].value.split()
    if index is None:
        assert "data-fragment-index" not in image.attributes
    else:
        assert index in image.attributes["data-fragment-index"].value
