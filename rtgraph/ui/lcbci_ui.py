
from PyQt5 import QtCore, QtGui, QtWidgets

class _qline(QtWidgets.QFrame):
    """Creates a line widget"""
    def __init__(self):
        super(_qline, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class main_ui(object):

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(720, 600)

        # create central widget and layout
        self.central_widget = QtWidgets.QWidget(MainWindow)
        self.central_widget.setObjectName("central_widget")
        self.central_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.central_layout.setObjectName("central_layout")

        # create main layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.main_layout.addWidget(QtWidgets.QLabel("lcbci lab v0.0.1"))

        # main layout: plot widget
        self.plt = GraphicsLayoutWidget()
        self.plt.setAutoFillBackground(False)
        self.plt.setStyleSheet("border: 0px;")
        self.plt.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.plt.setFrameShadow(QtWidgets.QFrame.Plain)
        self.plt.setLineWidth(0)
        self.plt.setMinimumWidth(600)
        self.plt.setObjectName("plt")
        self.main_layout.addWidget(self.plt)
        
        # main layout: console log
        self.tBrowser_Log = QtWidgets.QTextBrowser()
        self.tBrowser_Log.setFixedHeight(120)
        self.tBrowser_Log.setObjectName("tBrowser_Log")
        self.main_layout.addWidget(self.tBrowser_Log)

        # create control layout
        self.control_layout = QtWidgets.QVBoxLayout()
        self.control_layout.setObjectName("control_layout")
        self.control_layout.addWidget(QtWidgets.QLabel())

        # control layout: file options label
        self.qLabel_FileOptions = QtWidgets.QLabel("File Options")
        self.qLabel_FileOptions.setObjectName("qLabel_FileOptions")
        self.qLabel_FileOptions.setAlignment(QtCore.Qt.AlignCenter)
        self.control_layout.addWidget(self.qLabel_FileOptions)

        # control layout: open button
        self.pButton_Open = QtWidgets.QPushButton("Open")
        self.pButton_Open.setObjectName("pButton_Open")
        self.control_layout.addWidget(self.pButton_Open)

        # control layout: save button
        self.pButton_Save = QtWidgets.QPushButton("Save")
        self.pButton_Save.setObjectName("pButton_Save")
        self.control_layout.addWidget(self.pButton_Save)

        self.control_layout.addWidget(_qline()) # hline separator

        # control layout: control options label
        self.qLabel_ControlOptions = QtWidgets.QLabel("Control Options")
        self.qLabel_ControlOptions.setObjectName("qLabel_ControlOptions")
        self.qLabel_ControlOptions.setAlignment(QtCore.Qt.AlignCenter)
        self.control_layout.addWidget(self.qLabel_ControlOptions)

        # control layout: start button
        self.pButton_Start = QtWidgets.QPushButton("Start")
        self.pButton_Start.setObjectName("pButton_Start")
        self.control_layout.addWidget(self.pButton_Start)

        # control layout: stop button
        self.pButton_Stop = QtWidgets.QPushButton("Stop")
        self.pButton_Stop.setObjectName("pButton_Stop")
        self.control_layout.addWidget(self.pButton_Stop)

        # control layout: record button
        self.pButton_Record = QtWidgets.QPushButton("Record")
        self.pButton_Record.setObjectName("pButton_Record")
        self.control_layout.addWidget(self.pButton_Record)

        # control layout: play button
        self.pButton_Play = QtWidgets.QPushButton("Play")
        self.pButton_Play.setObjectName("pButton_Play")
        self.control_layout.addWidget(self.pButton_Play)

        self.control_layout.addWidget(_qline()) # hline separator

        # control layout: arduino options label
        self.qLabel_ArduinoOptions = QtWidgets.QLabel("Arduino Options")
        self.qLabel_ArduinoOptions.setObjectName("qLabel_ArduinoOptions")
        self.qLabel_ArduinoOptions.setAlignment(QtCore.Qt.AlignCenter)
        self.control_layout.addWidget(self.qLabel_ArduinoOptions)

        # control layout: refresh ports button
        self.pButton_RefreshPorts = QtWidgets.QPushButton("Refresh Ports")
        self.pButton_RefreshPorts.setObjectName("pButton_RefreshPorts")
        self.control_layout.addWidget(self.pButton_RefreshPorts)

        # control layout: port id combo box
        self.cBox_PortID = QtWidgets.QComboBox()
        self.cBox_PortID.setObjectName("cBox_PortID")
        self.control_layout.addWidget(self.cBox_PortID)

        # control layout: baud rate combo box
        self.cBox_BaudRate = QtWidgets.QComboBox()
        self.cBox_BaudRate.setObjectName("cBox_BaudRate")
        self.control_layout.addWidget(self.cBox_BaudRate)

        # control layout: connect button
        self.pButton_Connect = QtWidgets.QPushButton("Connect")
        self.pButton_Connect.setObjectName("pButton_Connect")
        self.control_layout.addWidget(self.pButton_Connect)

        self.control_layout.addWidget(_qline()) # hline separator

        # control layout: experiments label
        self.qLabel_Experiments = QtWidgets.QLabel("Experiments")
        self.qLabel_Experiments.setObjectName("qLabel_Experiments")
        self.qLabel_Experiments.setAlignment(QtCore.Qt.AlignCenter)
        self.control_layout.addWidget(self.qLabel_Experiments)

        # control layout: record 90s button 
        self.pButton_Record90s = QtWidgets.QPushButton("Record 90s")
        self.pButton_Record90s.setObjectName("pButton_Record90s")
        self.control_layout.addWidget(self.pButton_Record90s)

        self.control_layout.addStretch() # add stretch to bottom of controls

        # add main and control widgets to central
        self.central_layout.addLayout(self.main_layout)
        self.central_layout.addLayout(self.control_layout)
        MainWindow.setCentralWidget(self.central_widget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "lcbci lab"))
        # self.pButton_Stop.setText(_translate("MainWindow", "Stop"))
        # self.pButton_Start.setText(_translate("MainWindow", "Start"))
        # self.sBox_Samples.setSuffix(_translate("MainWindow", " samples"))
        # self.sBox_Samples.setPrefix(_translate("MainWindow", "Show "))
        # self.chBox_export.setText(_translate("MainWindow", "Export to CSV"))


from pyqtgraph import GraphicsLayoutWidget
