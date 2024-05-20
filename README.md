# PyFragments

Add animated figures to your [Quarto](https://quarto.org) presentations.

## Install

```
pip install pyfragments
```

## Example

A [Revealjs](https://quarto.org/docs/presentations/revealjs/)
presentation created with Quarto,
which displays an *animated* matplotlib figure:

![Animated figure](https://raw.githubusercontent.com/maurosilber/pyfragments/main/docs/animated_figure.gif)

This is created with the following code,
in a Quarto `.qmd` file.

````qmd
---
format: revealjs
---

## Example of an animated figure

Move to the next slide to see the transitions.

```{python}
# | output: asis
import matplotlib.pyplot as plt
from pyfragments import AnimatedFigure

with AnimatedFigure() as ani:
    plt.xlim(0, 10)
    plt.ylim(0, 10)
    for i in range(10):
        with ani.fragment():
            plt.scatter(i, i)

```
````

## SVG example

To use SVG images,
each call to a `matplotlib` function must include a group id (`gid`) with a value of `.fragment`.

Note: it is important to set `embed-resources: true`
in the YAML options.

````qmd
---
format: revealjs
embed-resources: true
---

## Example of an animated figure

Move to the next slide to see the transitions.

```{python}
import matplotlib.pyplot as plt
from pyfragments.svg import animate

plt.ioff()  # prevents automatic output of png figure

fig = plt.figure()
for i in range(10):
    plt.scatter(i, i, gid=".fragment")
animate(fig)
```
````

To change the order of fragments,
or make different elements appear at the same time,
use `.fragment-<num>`:

```python
plt.scatter(..., gid=".fragment-2")  # appears second
plt.scatter(..., gid=".fragment-1")  # appears first
plt.scatter(..., gid=".fragment-2")  # appears second
```

To allow animation of images,
such as with `plt.imshow`,
it is important to disable `image.composite_image`:
`plt.rc("image", composite_image=False)`.
