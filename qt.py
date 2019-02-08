"""Wrapper for importing Qt.

Flattens all Qt imports into a single package, so we can avoid *
imports without excessive verbosity.
"""

from Qt.QtCore import *
from Qt.QtGui import *
from Qt.QtWidgets import *
