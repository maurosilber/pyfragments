import matplotlib.pyplot as plt

from .. import AnimatedFigure, _warning_comment


def test_warning(capsys):
    fig = plt.figure()

    with AnimatedFigure(fig):
        pass
    assert _warning_comment in capsys.readouterr().out

    with AnimatedFigure(fig, add_warning_comment=False):
        pass
    assert _warning_comment not in capsys.readouterr().out
