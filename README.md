## Overview ##
A tool for exploring the behavior of PyQt/PySide widgets. It shows a
live instance of a single widget, and displays all signals as they are
emitted. Also includes a simple documentation browser.

## Setup ##
Clone the repository and run `pipenv install` to create an environment
with the required dependencies.

## Command-Line Usage ##
```
python explorer.py [-h] [--model COLUMNS] class_name
```

If your widget requires a model (e.g. `QTableView`, `QComboBox`), then
use the `--model` flag. This will create a model with the specified
number of columns, and fill in a few rows of dummy data.

## Python Usage ##
Make sure `explorer.py` is in your `PYTHONPATH`, and import it into
your Python code. Create a widget normally. Then launch the explorer
with: ```explorer.explore(mywidget)```


