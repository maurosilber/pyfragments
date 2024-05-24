from __future__ import annotations

import io
from typing import TYPE_CHECKING
from xml.dom import minidom

import IPython.display

if TYPE_CHECKING:
    from matplotlib.figure import Figure


def animate(fig: Figure, **savefig):
    """Animate figure annotated with gid=".fragment",

    To add a data-fragment-index="n", use gid=".fragment-n".

    Examples:
        fig = plt.figure()
        plt.plot(..., gid=".fragment")
        animate(fig)

        fig = plt.figure()
        plt.plot(..., gid=".fragment-2")  # appears second
        plt.plot(..., gid=".fragment-1")  # appears first
        animate(fig)
    """

    with io.BytesIO() as buf:
        fig.savefig(buf, format="svg", **savefig)
        svg = buf.getvalue()
    svg = extract_classes_from_gid(svg)
    return IPython.display.SVG(svg)


def _extract_classes_from_element(element: minidom.Element, /):
    try:
        gid: str = element.attributes["id"].value
    except KeyError:
        return

    classes, rest = [], []
    index = None
    for s in gid.split():
        if s.startswith(".fragment-"):
            index = s.removeprefix(".fragment-")
            classes.append("fragment")
        elif s.startswith("."):
            classes.append(s.removeprefix("."))
        elif len(s) > 0:
            rest.append(s)

    if len(rest) > 0:
        element.attributes["id"] = " ".join(set(rest))
    else:
        element.attributes.removeNamedItem("id")
    if len(classes) > 0:
        element.attributes["class"] = " ".join(set(classes))
    if index is not None:
        element.attributes["data-fragment-index"] = index


def _extract_classes_from_image(element: minidom.Element, /):
    """Image gid get a random string appended without a space."""
    try:
        gid: str = element.attributes["id"].value
    except KeyError:
        return

    before, frag, after = gid.partition(".fragment")
    element.attributes["id"].value = f"{before} {frag}{after}"
    return _extract_classes_from_element(element)


def extract_classes_from_gid(buf: bytes, /):
    dom = minidom.parseString(buf)
    for e in dom.getElementsByTagName("g"):
        _extract_classes_from_element(e)
    for e in dom.getElementsByTagName("image"):
        _extract_classes_from_element(e)
    with io.StringIO() as b:
        dom.writexml(b)
        return b.getvalue()
