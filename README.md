# pyfragments

[![Copier Badge][copier-badge]][copier-url]
[![Pixi Badge][pixi-badge]][pixi-url]
![License][license-badge]
[![CI Badge][ci-badge]][ci-url]
[![conda-forge Badge][conda-forge-badge]][conda-forge-url]
[![PyPI Badge][pypi-badge]][pypi-url]
[![Python version Badge][pypi-version-badge]][pypi-version-url]

Add animations to revealjs presentations from Python code-blocks.

## Example

A [Revealjs](https://quarto.org/docs/presentations/revealjs/)
presentation created with Quarto,
which shows matplotlib figure animated with fragments
(i.e., moving to the next slide):

![Animated scatterplot](https://raw.githubusercontent.com/maurosilber/pyfragments/main/docs/static/animated_png.gif)

This is created with the following code,
in a Quarto `.qmd` file.

````qmd
---
format: revealjs
---

## Animated scatterplot

Move to the next slide to see the transitions.

```{python}
# | output: asis
import matplotlib.pyplot as plt
from pyfragments.png import AnimatedFigure

with AnimatedFigure() as ani:
    plt.xlim(-1, 3)
    plt.ylim(-1, 3)
    for i in range(3):
        with ani.fragment():
            plt.scatter(i, i, s=200)

```
````

## Docs

See the demo in [GitHub Pages](https://maurosilber.github.io/pyfragments).

To change the order of fragments,
or make different elements appear at the same time,
use `ani.fragment(<num>)`:

```python
with ani.fragment(2):  # appears second
    ax.scatter(...)
with ani.fragment(1):  # appears first
    ax.scatter(...)
with ani.fragment(2):  # appears second
    ax.scatter(...)
```

### SVG

To use SVG images,
each call to a `matplotlib` function must include a group id (`gid`) with a value of `.fragment`.

````qmd
---
format: revealjs
---

# Example of an animated figure

## Animated scatterplot

Move to the next slide to see the transitions.

```{python}
from matplotlib.figure import Figure
from pyfragments.svg import animate

fig = Figure()
ax = fig.add_subplot()
for i in range(3):
    ax.scatter(i, i, gid=".fragment")
animate(fig)
```
````

To change the order of fragments,
or make different elements appear at the same time,
use `.fragment-<num>`:

```python
ax.scatter(..., gid=".fragment-2")  # appears second
ax.scatter(..., gid=".fragment-1")  # appears first
ax.scatter(..., gid=".fragment-2")  # appears second
```

To allow animation of images,
such as with `ax.imshow`,
it is important to disable `image.composite_image`:

```python
import matplotlib

matplotlib.rc("image", composite_image=False)
```

## Install

Using [pixi](pixi-url),
install from PyPI with:

```sh
pixi add --pypi pyfragments
```

or install the latest development version from GitHub with:

```sh
pixi add --pypi pyfragments@https://github.com/maurosilber/pyfragments.git
```

Otherwise,
use `pip` or your `pip`-compatible package manager:

```sh
pip install pyfragments  # from PyPI
pip install git+https://github.com/maurosilber/pyfragments.git  # from GitHub
```

## Development

This project is managed by [pixi](https://pixi.sh).
You can install it for development using:

```sh
git clone https://github.com/maurosilber/pyfragments
cd pyfragments
pixi run pre-commit-install
```

Pre-commit hooks are used to lint and format the project.

### Testing

Run tests using:

```sh
pixi run test
```

### Publishing to PyPI

When a tagged commit is pushed to GitHub,
the GitHub Action defined in `.github/workflows/ci.yml`
builds and publishes the package to PyPI.

Tag a commit and push the tags with:

```sh
git tag <my-tag>
git push --tags
```

Trusted publishing must be enabled once in [PyPI Publishing](https://pypi.org/manage/account/publishing/).
Fill the following values in the form:

```
PyPI Project Name: pyfragments
            Owner: maurosilber
  Repository name: pyfragments
    Workflow name: ci.yml
 Environment name: pypi
```

[ci-badge]: https://img.shields.io/github/actions/workflow/status/maurosilber/pyfragments/ci.yml
[ci-url]: https://github.com/maurosilber/pyfragments/actions/workflows/ci.yml
[conda-forge-badge]: https://img.shields.io/conda/vn/conda-forge/pyfragments?logoColor=white&logo=conda-forge
[conda-forge-url]: https://prefix.dev/channels/conda-forge/packages/pyfragments
[copier-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/copier-org/copier/master/img/badge/badge-black.json
[copier-url]: https://github.com/copier-org/copier
[license-badge]: https://img.shields.io/badge/license-MIT-blue
[pixi-badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json
[pixi-url]: https://pixi.sh
[pypi-badge]: https://img.shields.io/pypi/v/pyfragments.svg?logo=pypi&logoColor=white
[pypi-url]: https://pypi.org/project/pyfragments
[pypi-version-badge]: https://img.shields.io/pypi/pyversions/pyfragments?logoColor=white&logo=python
[pypi-version-url]: https://pypi.org/project/pyfragments
