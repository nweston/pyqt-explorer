import docscraper
import os.path
import pathlib
import unittest
import qt


class TestDocScraper(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        base = os.path.dirname(__file__)
        cls.docfiles = [pathlib.Path(os.path.join(base, p)).read_text()
                        for p in ['QComboBox.html', 'QWidget.html']]

    def test_doc_urls(self):
        _ = qt.QApplication([])
        w = qt.QWidget()
        self.assertEqual(
            docscraper.doc_urls(w),
            ['https://doc.qt.io/qtforpython/PySide2/QtWidgets/QWidget.html',
             'https://doc.qt.io/qtforpython/PySide2/QtCore/QObject.html',
             'https://doc.qt.io/qtforpython/PySide2/QtGui/QPaintDevice.html'])

    def test_constructor(self):
        docscraper.DocScraper(self.docfiles)

    def test_method_doc_direct(self):
        scraper = docscraper.DocScraper(self.docfiles)
        result = scraper.get_doc('duplicatesEnabled')
        self.assertTrue(result.startswith('<dl class="method"'))
        self.assertIn(('dt id="PySide2.QtWidgets.PySide2.'
                       'QtWidgets.QComboBox.duplicatesEnabled"'),
                      result)

    def test_method_doc_inherited(self):
        scraper = docscraper.DocScraper(self.docfiles)
        result = scraper.get_doc('acceptDrops')
        self.assertTrue(result.startswith('<dl class="method"'))
        self.assertIn(('dt id="PySide2.QtWidgets.PySide2.'
                       'QtWidgets.QWidget.acceptDrops"'),
                      result)
