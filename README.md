# PyFragments

Add animated figures to your [Quarto](https://quarto.org) presentations.

## Install

```
pip install pyfragments
```

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
title: " "
format: revealjs
---

## Animated scatterplot

Move to the next slide to see the transitions.

```{python}
# | output: asis
import matplotlib.pyplot as plt
from pyfragments import AnimatedFigure

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

Note: it is important to set `embed-resources: true`
in the YAML options.

````qmd
---
format: revealjs
embed-resources: true
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
