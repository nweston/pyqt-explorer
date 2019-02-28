import qt
import requests
import docscraper
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


def signal_names(qobj):
    """Return names of all signals of an object."""

    # Figure out the type of signal objects. We can't hard-code this
    # because it depends on the underlying Qt wrapper.
    signal_type = type(qt.QPushButton().clicked)
    return [name for name in dir(qobj)
            if isinstance(getattr(qobj, name), signal_type)]


def create_scraper(widget):
    """Create a DocScraper with docs for widget and its superclasses."""
    docs = []
    for url in docscraper.doc_urls(widget):
        r = requests.get(url)
        if r.ok:
            # r.encoding is ISO-8859-1 for some reason, but this
            # appears to be UTF-8.
            docs.append(r.content.decode(encoding='utf-8'))
    return docscraper.DocScraper(docs)


class ExplorerWidget(qt.QWidget):
    """Interactively explores the operation of a single widget.

Displays signals as they are emitted, along with members and
documentation."""

    def __init__(self, widget, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.widget = widget
        widget.setParent(self)

        scraper = create_scraper(widget)

        output = qt.QTextEdit(parent=self)
        output.setReadOnly(True)
        clear_output = qt.QPushButton(
            parent=self, text='Clear', clicked=output.clear)
        clear_output.setAutoDefault(False)

        doc = qt.QTextEdit(parent=self)

        members = qt.QTreeWidget(parent=self)
        members.setHeaderHidden(True)
        members.itemClicked.connect(
            lambda i: doc.setHtml(scraper.get_doc(i.text(0))))
        self._populate_members(members, widget)

        HBox(
            self, margin=10,
            children=[
                # Left side
                VBox(children=[50,
                               widget,
                               50,
                               output,
                               clear_output]),
                # Right side
                VBox(children=[members,
                               doc])])

        self._connect_widget_signals(output)

    def _connect_widget_signals(self, output):
        def display_signal(name, *args):
            output.append('%s(%s)' % (name, ', '.join(map(str, args))))

        for name in signal_names(self.widget):
            sig = getattr(self.widget, name)
            sig.connect(partial(display_signal, name))

    def _populate_members(self, members, widget):
        signal_set = set(signal_names(widget))
        constants = []
        enums = []
        signals = []
        methods = []

        for name in sorted(dir(widget)):
            if not name.startswith('_'):
                m = getattr(widget, name)
                if name in signal_set:
                    signals.append(name)
                elif isinstance(m, type):
                    enums.append(name)
                elif callable(m):
                    methods.append(name)
                else:
                    constants.append(name)

        def add_top_level(name, children):
            item = qt.QTreeWidgetItem([name])
            item.addChildren([qt.QTreeWidgetItem([c]) for c in children])
            members.addTopLevelItem(item)
        add_top_level('Constants', constants)
        add_top_level('Enums', enums)
        add_top_level('Signals', signals)
        add_top_level('Methods', methods)


class ExplorerDialog(qt.QDialog):
    """A Dialog containing an ExplorerWidget."""

    def __init__(self, widget, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._explorer = ExplorerWidget(widget)
        self.setMinimumSize(1200, 1000)
        HBox(self, children=[self._explorer])


def explore(widget):
    """Create and execute an explorer dialog."""
    dialog = ExplorerDialog(widget)
    dialog.exec_()


if __name__ == '__main__':
    app = qt.QApplication([])
    w = qt.QComboBox()
    w.setEditable(True)
    for s in ['foo', 'bar', 'baz']:
        w.addItem(s)
    explore(w)
