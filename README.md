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

````
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
