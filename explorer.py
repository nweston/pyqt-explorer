import qt
from functools import partial


class EasyLayout():
    """Base class for layout wrappers.

These wrappers provide several conveniences:

1. Constructor takes margin as a keyword argument so it can easily be
   changed.

2. Margin defaults to zero to prevent ever-increasing padding as
   layouts are nested.

3. Constructor takes children as a keyword argument. This is a list of
   QWidgets and QLayouts, all of which will be added with the
   appropriate method calls.

The combination of these features can condense many lines of
addLayout/addWidget/setMargin calls into a few nested calls, with a
structure that visually reflects the layout.
    """

    def _setup(self, margin, children):
        """Set up layout by setting margin and adding all children.

Children may be QWidgets or QLayouts."""

        self.setMargin(margin)
        for c in children:
            if isinstance(c, qt.QWidget):
                self.addWidget(c)
            elif isinstance(c, int):
                self.addSpacing(c)
            else:
                self.addLayout(c)


class HBox(qt.QHBoxLayout, EasyLayout):
    """Convenience wrapper for QHBoxLayout."""

    def __init__(self, parent=None, margin=0, children=[], **kwargs):
        """Initialize layout, set margin and adding children."""
        super().__init__(parent)
        self._setup(margin, children)


class VBox(qt.QVBoxLayout, EasyLayout):
    """Convenience wrapper for QVBoxLayout."""

    def __init__(self, parent=None, margin=0, children=[], **kwargs):
        """Initialize layout, set margin and adding children."""
        super().__init__(parent)
        self._setup(margin, children)


def signals(qobj):
    """Return names of all signals of an object."""

    # Figure out the type of signal objects. We can't hard-code this
    # because it depends on the underlying Qt wrapper.
    signal_type = type(qt.QPushButton().clicked)
    return [name for name in dir(qobj)
            if isinstance(getattr(qobj, name), signal_type)]


class ExplorerWidget(qt.QWidget):
    def __init__(self, widget, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.widget = widget
        widget.setParent(self)
        self._output = qt.QTextEdit(parent=self)
        self._output.setReadOnly(True)
        clear_output = qt.QPushButton(
            parent=self, text='Clear', clicked=self._output.clear)
        clear_output.setAutoDefault(False)

        HBox(
            self, margin=10,
            children=[
                # Left side
                VBox(children=[widget,
                               self._output,
                               clear_output]),
                # Right side
                VBox(children=[qt.QLabel('members'),
                               qt.QLabel('doc')])])

        self._connect_widget_signals()

    def _connect_widget_signals(self):
        def display_signal(name, *args):
            self._output.append('%s(%s)' %
                                (name, ', '.join(map(str, args))))

        for name in signals(self.widget):
            sig = getattr(self.widget, name)
            sig.connect(partial(display_signal, name))


class ExplorerDialog(qt.QDialog):
    def __init__(self, widget, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._explorer = ExplorerWidget(widget)
        HBox(self, children=[self._explorer])


def explore(widget):
    dialog = ExplorerDialog(widget)
    dialog.exec_()


if __name__ == '__main__':
    app = qt.QApplication([])
    w = qt.QComboBox()
    w.setEditable(True)
    for s in ['foo', 'bar', 'baz']:
        w.addItem(s)
    explore(w)
