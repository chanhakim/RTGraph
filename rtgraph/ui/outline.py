from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import pyqtgraph as pg
import pyqtgraph.exporters

class _qline(QFrame):
    """Creates a line widget"""
    def __init__(self):
        super(_qline, self).__init__()
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)

class _buttons(QWidget):
    """A class for holding the control buttons"""

    def __init__(self):
        super(_buttons, self).__init__()
        self._create_buttons()
        self._create_widget()

    def _create_buttons(self):
        self.file = {
            'open': QPushButton('Open'),
            'save': QPushButton('Save')
        }
        self.control = {
            'start': QPushButton('Start'),
            'stop': QPushButton('Stop'),
            'record': QPushButton('Record'),
            'play': QPushButton('Play'),
        }
        self.arduino = {
            'refresh_ports': QPushButton('Refresh ports'),
            'port': QComboBox(),
            'baud': QComboBox(),
            'connect': QPushButton('Connect')
        }
        self.arduino['port'].addItem('Port ID')
        self.arduino['baud'].addItems([str(num) for num in ['Baud Rate', 9600, 14400, 19200, 28800, 38400, 57600, 115200]])
        self.arduino['port'].setFixedWidth(120)
        self.arduino['baud'].setFixedWidth(120)
        self.experiments = {
            'record_90s': QPushButton('Record 90s')
        }

    def _create_widget(self):
        layout = QVBoxLayout()
        file_label = QLabel('File Options')
        file_label.setAlignment(Qt.AlignCenter)
        control_label = QLabel('Control Options')
        control_label.setAlignment(Qt.AlignCenter)
        arduino_label = QLabel('Arduino Options')
        arduino_label.setAlignment(Qt.AlignCenter)
        experiments_label = QLabel('Experiments')
        experiments_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(QLabel(' '))
        layout.addWidget(file_label)
        for button in list(self.file.values()):
            layout.addWidget(button)
        layout.addWidget(_qline())
        layout.addWidget(control_label)
        for button in list(self.control.values()):
            layout.addWidget(button)
        layout.addWidget(_qline())
        layout.addWidget(arduino_label)
        for button in list(self.arduino.values()):
            layout.addWidget(button)
        layout.addWidget(_qline())
        layout.addWidget(experiments_label)
        for button in list(self.experiments.values()):
            layout.addWidget(button)

        layout.addStretch()
        self.setLayout(layout)
        
class _graphs(QWidget):
    """A class for holding the graph and folder dialog"""
    def __init__(self):
        super(_graphs, self).__init__()
        self._create_elements()
        self._place_elements()

    def _create_elements(self):
        self.graph = pg.plot()
        self.graph.setMinimumWidth(600)
        self.console = QTextBrowser()
        self.console.setFixedHeight(120)

    def _place_elements(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('lcbci lab v0.1'))
        layout.addWidget(self.graph)
        layout.addWidget(self.console)
        self.setLayout(layout)
   
class lcbci_widgets(QMainWindow):
    def __init__(self):
        super(lcbci_widgets, self).__init__()
        self._configure_ui()
        self._add_widgets()

    def _configure_ui(self):
        self.setWindowTitle('lcbci lab v0.1')
        self.setWindowIcon(QIcon('logo.png'))
        self.resize(780, 600)

    def _save_widgets(self, main, buttons):
        self.open = buttons.file['open']
        self.save = buttons.file['save']
        self.start = buttons.control['start']
        self.stop = buttons.control['stop']
        self.record = buttons.control['record']
        self.play = buttons.control['play']
        self.refresh_ports = buttons.arduino['refresh_ports']
        self.port = buttons.arduino['port']
        self.baud = buttons.arduino['baud']
        self.connect = buttons.arduino['connect']
        self.record90s = buttons.experiments['record_90s']

        self.graph = main.graph
        self.console = main.console
        
        self.file_dg = pg.widgets.FileDialog.FileDialog()
        self.exporter = pg.exporters.CSVExporter(self.graph.plotItem)
        self.timer = pg.QtCore.QTimer()


    def _add_widgets(self):
        main, buttons = _graphs(), _buttons()
        self._save_widgets(main, buttons)

        layout = QHBoxLayout()
        layout.addWidget(main)
        layout.addWidget(buttons)

        widget = QWidget()
        widget.setLayout(layout)

        self.setCentralWidget(widget)