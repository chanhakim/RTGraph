from multiprocessing import freeze_support
import sys
from PyQt5 import QtGui

from lcbci_lab.common.architecture import Architecture
from lcbci_lab.common.arguments import *
from lcbci_lab.common.logger import Logger as Log
from lcbci_lab.core.constants import MinimalPython
from lcbci_lab.ui import mainWindow


TAG = "lcbci_lab"


class lcbci_lab:
    def __init__(self, argv=sys.argv):
        freeze_support()
        self._args = self._init_logger()
        self._app = QtGui.QApplication(argv)

    def run(self):
        if Architecture.is_python_version(MinimalPython.major, minor=MinimalPython.minor):
            Log.i(TAG, "Starting lcbci_lab")
            win = mainWindow.MainWindow(samples=self._args.get_user_samples())
            win.setWindowTitle("{} - {}".format(Constants.app_title, Constants.app_version))
            win.show()
            self._app.exec()
            Log.i(TAG, "Finishing lcbci_lab\n")
            win.close()
        else:
            self._fail()
        self.close()

    def close(self):
        self._app.exit()
        Log.close()
        sys.exit()

    @staticmethod
    def _init_logger():
        args = Arguments()
        args.create()
        args.set_user_log_level()
        return args

    @staticmethod
    def _fail():
        txt = str("lcbci_lab requires Python {}.{} to run"
                  .format(MinimalPython.major, MinimalPython.minor))
        Log.e(TAG, txt)


if __name__ == '__main__':
    lcbci_lab().run()
