from datetime import datetime

from PyQt5 import QtWidgets, uic
import logging

from PyQt5.QtWidgets import QDialog

from src.models import TimeRecord


class EditRecordDialog(QtWidgets.QDialog):
    def __init__(self, parent, data: TimeRecord):
        # Call the inherited classes __init__ method
        super().__init__(parent)
        uic.loadUi('src/EditRecord.ui', self)
        logging.info('Loaded edit record dialog...')

        self.model = data

        self.dateEdit.setDateTime(data.start)
        self.timeEditStart.setDateTime(data.start)
        self.timeEditEnd.setDateTime(data.end)

    def accept(self):
        date = self.dateEdit.dateTime().date()
        start = self.timeEditStart.dateTime().time()
        end = self.timeEditEnd.dateTime().time()

        self.model.start = datetime(
            date.year(),
            date.month(),
            date.day(),
            start.hour(),
            start.minute())

        self.model.end = datetime(
            date.year(),
            date.month(),
            date.day(),
            end.hour(),
            end.minute())

        QDialog.accept(self)