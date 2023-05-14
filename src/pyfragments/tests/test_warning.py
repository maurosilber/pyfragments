import matplotlib.pyplot as plt

from .. import _warning_comment, animated_figure


def test_warning(capsys):
    fig = plt.figure()

    with animated_figure(fig):
        pass
    assert _warning_comment in capsys.readouterr().out

    with animated_figure(fig, add_warning_comment=False):
        pass
    assert _warning_comment not in capsys.readouterr().out
