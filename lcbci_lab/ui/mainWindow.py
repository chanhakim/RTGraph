from lcbci_lab.ui.lcbci_ui import *

from lcbci_lab.core.worker import Worker
from lcbci_lab.core.constants import Constants, SourceType
from lcbci_lab.ui.popUp import PopUp
from lcbci_lab.common.logger import Logger as Log


TAG = "MainWindow"


class MainWindow(QtGui.QMainWindow):
    """
    Handles the ui elements and connects to worker service to execute processes.
    """
    def __init__(self, port=None, bd=115200, samples=1000):
        """
        Initializes values for the UI.
        :param port: Default port name to be used. It will also disable scanning available ports.
        :type port: str.
        :param bd: Default baud rate to be used. It will be added to the common baud rate list if not available.
        :type bd: int.
        :param samples: Default samples per second to be shown in the plot.
        :type samples: int.
        """
        QtGui.QMainWindow.__init__(self)
        self.ui = main_ui()
        self.ui.setup_ui(self)

        # Shared variables, initial values
        self._plt = None
        self._timer_plot = None
        self.worker = Worker()

        # configures
        # self.ui.cBox_Source.addItems(Constants.app_sources)
        self._configure_plot()
        self._configure_timers()
        self._configure_signals()

        self.ui.sBox_Samples.setValue(samples)

        # enable ui
        self._enable_ui(True)

    def start(self):
        """
        Starts the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Start button.
        :return:
        """
        Log.i(TAG, "Clicked start")
        port_id, baud_rate = self.ui.cBox_Port.currentText(), self.ui.cBox_BaudRate.currentText()
        if (port_id != "Ports (Refresh)") and (baud_rate != "Baud Rate"):
            self.worker = Worker(port=self.ui.cBox_Port.currentText(),
                                speed=int(self.ui.cBox_BaudRate.currentText()),
                                samples=self.ui.sBox_Samples.value())
            if self.worker.start():
                self._timer_plot.start(Constants.plot_update_ms)
                self._enable_ui(False)
            else:
                Log.i(TAG, "Port is not available")
                PopUp.warning(self, Constants.app_title, "Selected port \"{}\" is not available"
                            .format(self.ui.cBox_Port.currentText()))
        else:
            Log.i(TAG, "No port or baud rate was selected")
            PopUp.warning(self, Constants.app_title, "Select a port and baud rate")
        

    def stop(self):
        """
        Stops the acquisition of the selected serial port.
        This function is connected to the clicked signal of the Stop button.
        :return:
        """
        Log.i(TAG, "Clicked stop")
        self._timer_plot.stop()
        self._enable_ui(True)
        self.worker.stop()

    def record(self):
        """
        Starts recording signal from the selected port. Function
        is connected to the record button
        :return:
        """
        Log.i(TAG, "Clicked record")
        port_id, baud_rate = self.ui.cBox_Port.currentText(), self.ui.cBox_BaudRate.currentText()
        if (port_id != "Ports (Refresh)") and (baud_rate != "Baud Rate"):
            self.worker = Worker(port=self.ui.cBox_Port.currentText(),
                                speed=int(self.ui.cBox_BaudRate.currentText()),
                                samples=self.ui.sBox_Samples.value(),
                                export_enabled=True)
            if self.worker.start():
                self._timer_plot.start(Constants.plot_update_ms)
                self._enable_ui(False)
            else:
                Log.i(TAG, "Port is not available")
                PopUp.warning(self, Constants.app_title, "Selected port \"{}\" is not available"
                            .format(self.ui.cBox_Port.currentText()))
        else:
            Log.i(TAG, "No port or baud rate was selected")
            PopUp.warning(self, Constants.app_title, "Select a port and baud rate")

    def record90s(self):
        """
        Records 90 seconds of signal from the selected port.
        :return:
        """
        # either use the time module and run start -> stop for 90s
        # or compute the number of samples to be taken over the course of time
        # (e.g., for a 90s recording at 200 hz, 90*200 samples should be taken)
        None

    def closeEvent(self, evnt):
        """
        Overrides the QTCloseEvent.
        This function is connected to the clicked signal of the close button of the window.
        :param evnt: QT evnt.
        :return:
        """
        if self.worker.is_running():
            Log.i(TAG, "Window closed without stopping capture, stopping it")
            self.stop()

    def _enable_ui(self, enabled):
        """
        Enables or disables the UI elements of the window.
        :param enabled: The value to be set at the enabled characteristic of the UI elements.
        :type enabled: bool
        :return:
        """
        self.ui.cBox_Port.setEnabled(enabled)
        self.ui.cBox_BaudRate.setEnabled(enabled)
        self.ui.pButton_Start.setEnabled(enabled)
        self.ui.pButton_Stop.setEnabled(not enabled)
        self.ui.pButton_Record.setEnabled(enabled)
        self.ui.pButton_Save.setEnabled(enabled)

    def _configure_plot(self):
        """
        Configures specific elements of the PyQtGraph plots.
        :return:
        """
        # self.ui.plt.setBackground(background=None)
        self.ui.plt.setAntialiasing(True)
        self._plt = self.ui.plt.addPlot(row=1, col=1)
        self._plt.setLabel('bottom', Constants.plot_xlabel_title, Constants.plot_xlabel_unit)

    def _configure_timers(self):
        """
        Configures specific elements of the QTimers.
        :return:
        """
        self._timer_plot = QtCore.QTimer(self)
        self._timer_plot.timeout.connect(self._update_plot)

    def _configure_signals(self):
        """
        Configures the connections between signals and UI elements.
        :return:
        """
        self.ui.pButton_Start.clicked.connect(self.start)
        self.ui.pButton_Stop.clicked.connect(self.stop)
        self.ui.pButton_Record.clicked.connect(self.record)
        self.ui.cBox_Port.activated.connect(self._update_port)
        self.ui.sBox_Samples.valueChanged.connect(self._update_sample_size)
        # self.ui.cBox_Source.currentIndexChanged.connect(self._source_changed)

        self._update_port()

    def _update_sample_size(self):
        """
        Updates the sample size of the plot.
        This function is connected to the valueChanged signal of the sample Spin Box.
        :return:
        """
        if self.worker is not None:
            Log.i(TAG, "Changing sample size")
            self.worker.reset_buffers(self.ui.sBox_Samples.value())

    def _update_plot(self):
        """
        Updates and redraws the graphics in the plot.
        This function us connected to the timeout signal of a QTimer.
        :return:
        """
        self.worker.consume_queue()

        # plot data
        self._plt.clear()
        for idx in range(self.worker.get_lines()):
            self._plt.plot(x=self.worker.get_time_buffer(),
                           y=self.worker.get_values_buffer(idx),
                           pen=Constants.plot_colors[idx])

    def _update_port(self):
        """
        Updates the source and depending boxes on change.
        This function is connected to the indexValueChanged signal of the Source ComboBox.
        :return:
        """
        tmp = self.ui.cBox_Port.currentText()
        if  tmp == "Ports (Refresh)":
            Log.i(TAG, "Scanning source serial")
            # clear boxes before adding new
            self.ui.cBox_Port.clear()

            ports = self.worker.get_source_ports(SourceType.serial)
            ports.insert(0, "Ports (Refresh)")

            if ports is not None:
                self.ui.cBox_Port.addItems(ports)
        else:
            Log.i(TAG, "Serial port {} was selected".format(tmp))


