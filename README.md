# mBCI Lab

## Description

mBCI Lab v0.0.1 is a fork of RTGraph and introduces a new graphical user interface and a timed-recording feature. It is part of the mBCI project (https://github.com/chanhakim/mbci).

### Dependencies

The following dependencies can be installed with pip.

- Python 3
- PyQt5
- PySerial
- PyQtGraph

### Installation via Pip

```shell
pip install PyQt5 pyqtgraph pyserial
```

### Running the Program

```shell
python -m mbci_lab
```

or

```
sh ./mbci_lab.sh
```

------

Below is a copy of the original README from RTGraph.

## RTGraph

A simple Python application for plotting and storing data from a serial port in real time, formatted as [CSV](https://en.wikipedia.org/wiki/Comma-separated_values).
The application uses the [mutliprocessing](https://docs.python.org/3/library/multiprocessing.html) package to allow better usage of the host resources, overcoming limitations such as [GIL](https://docs.python.org/3/glossary.html#term-global-interpreter-lock) in Python.  

### Dependencies

- Python 3 (3.2 or later).
- PyQt5.
- PySerial.
- [PyQtGraph](http://www.pyqtgraph.org/).

### Installation instructions

#### Using Anaconda or Miniconda (Windows, macOS, Linux)

1. Install [Anaconda](https://www.continuum.io/downloads) or [Miniconda](https://conda.io/miniconda.html). Remember to add conda to your path.
2. Open a terminal and type:
    - `conda install pyqtgraph pyserial`

#### Using Pip (Windows, macOS, Linux)

1. Verify you have installed pip.
2. Open a terminal and type:
    - `pip install PyQt5 pyqtgraph pyserial`

#### Linux (Apt based distros)

1. Open a terminal and type:
    - `sudo apt-get install python3-pyqt5 python3-pyqtgraph python3-serial`

### Usage

From a terminal, on the root folder of the project, run:
- `python -m rtgraph`

### Links

- [Presentation on SciPy 2015](https://www.youtube.com/watch?v=yNOJ_NfzI64&index=1&list=PLiOqvn0zxKhOy6WKGYMz3wHxJRN_zGCvD&t=896s)
- [Proceedings on SciPy 2015](http://conference.scipy.org/proceedings/scipy2015/pdfs/sebastian_sepulveda.pdf)

### License and Citations

The project is distributed under MIT License. A DOI is attached to the project for citations.
[![DOI](https://zenodo.org/badge/doi/10.5281/zenodo.12789.svg)](http://dx.doi.org/10.5281/zenodo.12789)