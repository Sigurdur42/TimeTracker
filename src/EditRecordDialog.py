from datetime import datetime

from PyQt6 import QtWidgets
import logging

from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QDateEdit, QTimeEdit, QDialogButtonBox, QLayout, \
    QCheckBox

from src.models import TimeRecord


class EditRecordDialog(QtWidgets.QDialog):
    def __init__(self, parent, data: TimeRecord):
        # Call the inherited classes __init__ method
        super().__init__(parent)

        logging.info('Creating edit record dialog...')
        self.setWindowTitle("Edit record")
        form_layout = QFormLayout()

        self.dateEdit = QDateEdit()
        form_layout.addRow("Date:", self.dateEdit)

        self.timeEditStart = QTimeEdit()
        form_layout.addRow("Start:", self.timeEditStart)

        self.timeEditEnd = QTimeEdit()
        form_layout.addRow("End:", self.timeEditEnd)

        self.allOvertimeCheck = QCheckBox()
        form_layout.addRow("All Overtime:", self.allOvertimeCheck)

        outer_layout = QVBoxLayout()
        outer_layout.addLayout(form_layout)

        button_box = QVBoxLayout()
        dialog_button_box = (
            QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel))

        ok_button = dialog_button_box.button(QDialogButtonBox.StandardButton.Ok)
        ok_button.clicked.connect(self.my_accept)
        dialog_button_box.rejected.connect(self.reject)

        button_box.addWidget(dialog_button_box)
        outer_layout.addLayout(button_box)

        outer_layout.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setLayout(outer_layout)

        self.model = data

        self.dateEdit.setDateTime(data.start)
        self.timeEditStart.setTime(data.start.time())
        self.timeEditEnd.setTime(data.end.time())
        self.allOvertimeCheck.setChecked(data.all_overtime)

    def my_accept(self, checked=False):
        date = self.dateEdit.dateTime().date()
        start = self.timeEditStart.dateTime().time()
        end = self.timeEditEnd.dateTime().time()

        self.model.all_overtime = self.allOvertimeCheck.isChecked()
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
