import shutil

from mbci_lab.ui.mbci_ui import *

from mbci_lab.core.worker import Worker
from mbci_lab.core.constants import Constants, SourceType
from mbci_lab.ui.popUp import PopUp
from mbci_lab.common.logger import Logger as Log

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
        self.session_files = []

        # Shared variables, initial values
        self._plt = None
        self._timer_plot = None
        self._isrecording = False
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
        self.ui.tBrowser_Log.append("Started data stream.")
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
            self.ui.tBrowser_Log.append("Terminated data stream due to error.")
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
        self.session_files.append(self.worker.get_filepath())
        if self._isrecording == True:
            self._isrecording = False
            self.save()
        self.ui.tBrowser_Log.append("Stopped data stream.")

    def record(self):
        """
        Starts recording signal from the selected port. Function
        is connected to the record button
        :return:
        """
        Log.i(TAG, "Clicked record")
        self.ui.tBrowser_Log.append("Started recording data.")
        self._isrecording = True
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
                return None
        else:
            Log.i(TAG, "No port or baud rate was selected")
            self.ui.tBrowser_Log.append("Terminated data recording due to error.")
            PopUp.warning(self, Constants.app_title, "Select a port and baud rate")
            return None

    def recordNs(self):
        """
        Records N seconds of signal from the selected port.
        :return:
        """
        self.record()
        if self.ui.sBox_Seconds.value() > 0:
            QtCore.QTimer.singleShot(self.ui.sBox_Seconds.value()*1000+100, self.stop) # add 100 ms to off-set buffer

    def save(self):
        """
        Saves the recorded file to the desired location.
        :return:
        """
        Log.i(TAG, "Clicked save")
        if len(self.session_files) > 0:
            save_path = PopUp.save_file(self)
            if save_path != '':
                Log.i(TAG, "Saving {} at {}".format(self.session_files[-1], save_path))
                shutil.copyfile(self.session_files[-1], save_path)
                Log.i(TAG, "Saved {} at {}".format(self.session_files[-1], save_path))
                self.ui.tBrowser_Log.append("Saved data at {}.".format(save_path))
            else:
                Log.i(TAG, "No file name entered, so file wasn't saved.")
        else:
            Log.i(TAG, "No signal files in current session.")
            self.ui.tBrowser_Log.append("Terminated save due to an error.")
            PopUp.warning(self, Constants.app_title, "Record signal before saving.")
        

    def help(self):
        """
        Opens the message for the program.
        This function is connected to the clicked signal of the Help button.
        :return:
        """
        Log.i(TAG, "Clicked help")
        PopUp.message(self, Constants.app_title + " Instructions", "View Options:\n     - Start: starts data stream\n     - Stop: stops data stream\n\nRecord Options\n     - n Seconds: enter the desired time length\n     - Record: starts recording data\n     - Save: save recorded data\n\nBCI/Plot Options\n     - Ports: select the serial device port\n     - Baud Rate: select the baud rate\n     - n Samples: enter the desired samples #")

    def closeEvent(self, evnt):
        """
        Overrides the QTCloseEvent.
        This function is connected to the clicked signal of the close button of the window.
        :param evnt: QT evnt.
        :return:
        """
        if self.worker.is_running():
            Log.i(TAG, "Window closed without stopping capture, stopping it")
            self.ui.tBrowser_Log.append("Closing window.")
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
        self.ui.sBox_Samples.setEnabled(enabled)
        self.ui.sBox_Seconds.setEnabled(enabled)

    def _configure_plot(self):
        """
        Configures specific elements of the PyQtGraph plots.
        :return:
        """
        self.ui.plt.setBackground(background=[34,34,34,255])
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
        self.ui.pButton_Record.clicked.connect(self.recordNs)
        self.ui.pButton_Save.clicked.connect(self.save)
        self.ui.cBox_Port.activated.connect(self._update_port)
        self.ui.sBox_Samples.valueChanged.connect(self._update_sample_size)
        self.ui.sBox_Seconds.valueChanged.connect(self._update_seconds)
        self.ui.cBox_BaudRate.activated.connect(self._update_baud)
        self.ui.pButton_Help.clicked.connect(self.help)

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
            self.ui.tBrowser_Log.append("Updated sample size: {}.".format(self.ui.sBox_Samples.value()))

    def _update_seconds(self):
        """
        Updates the seconds for recording.
        This function is connected to the valueChanged signal of the sample Spin Box.
        :return:
        """
        if self.worker is not None:
            Log.i(TAG, "Changing recording length")
            self.worker.reset_buffers(self.ui.sBox_Seconds.value())
            self.ui.tBrowser_Log.append("Updated recording length: {} seconds.".format(self.ui.sBox_Seconds.value()))

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
            self.ui.tBrowser_Log.append("Refreshed ports.")
        else:
            Log.i(TAG, "Serial port {} was selected".format(tmp))
            self.ui.tBrowser_Log.append("Selected port: {}".format(self.ui.cBox_Port.currentText()))

    def _update_baud(self):
        """
        Updates the baud rate.
        :return:
        """
        if self.ui.cBox_BaudRate.currentText() == "Baud Rate":
            Log.i(TAG, "No baud rate selected")
            self.ui.tBrowser_Log.append("No baud rate was selected.")
        else:
            Log.i(TAG, "Updated baud rate: {}".format(self.ui.cBox_BaudRate.currentText()))
            self.ui.tBrowser_Log.append("Updated baud rate: {}.".format(self.ui.cBox_BaudRate.currentText()))