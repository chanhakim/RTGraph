from PyQt5 import QtGui
from pathlib import Path
import datetime

class PopUp:
    @staticmethod
    def question_yes_no(parent, title, message):
        """
        Shows a Pop up question dialog with yes and no buttons.
        :param parent: Parent window for the dialog.
        :param title: Title of the dialog.
        :type title: str.
        :param message: Message to be shown in the content of the dialog.
        :type message: str.
        :return: True if the Yes button was pressed in the dialog.
        :rtype: bool.
        """
        ans = QtGui.QMessageBox.question(parent,
                                         title,
                                         message,
                                         QtGui.QMessageBox.Yes,
                                         QtGui.QMessageBox.No)
        if ans == QtGui.QMessageBox.Yes:
            return True
        else:
            return False

    @staticmethod
    def warning(parent, title, message):
        """
        Shows a Pop up warning dialog with a Ok buttons.
        :param parent: Parent window for the dialog.
        :param title: Title of the dialog.
        :type title: str.
        :param message: Message to be shown in the content of the dialog.
        :type message: str.
        :return:
        """
        QtGui.QMessageBox.warning(parent, title, message, QtGui.QMessageBox.Ok)

    @staticmethod
    def save_file(parent):
        """
        Shows a popup window for saving the file at a desired path with name.
        :return filepath:
        :rtype str:
        """
        file_name, _ = QtGui.QFileDialog.getSaveFileName(parent, caption='Save File', directory='{path}/lcbci_recording_{date}'.format(path=str(Path.home()), date=datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')), filter='*.csv')
        return file_name