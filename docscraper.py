"""Extract documentation from PySide2 API docs.
"""
import re
from bs4 import BeautifulSoup


def doc_urls(obj):
    """Return documentation URLs for obj and all its Qt superclasses."""
    pyside_base = 'https://doc.qt.io/qtforpython/PySide2'
    result = []
    for t in type(obj).mro():
        if t.__module__.startswith('PySide2.'):
            module_name = t.__module__.replace('PySide2.', '')
            result.append(f'{pyside_base}/{module_name}/{t.__name__}.html')
    return result


class DocScraper:
    def __init__(self, docfiles):
        """Create a DocScraper to process the given files.

Documentation lookup will check each file in the order they are passed
to the constructor.
        """
        self._doms = [BeautifulSoup(d, features='html.parser')
                      for d in docfiles]

    def get_doc(self, name):
        """Return HTML documentation for a member."""

        for dom in self._doms:
            result = dom.find('dt', id=re.compile(f'.*\\.{name}$'))
            if result:
                return str(result.parent)
        return None
