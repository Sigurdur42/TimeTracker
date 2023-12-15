import logging
import os

from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import Qt
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtGui import QColor, QPalette, QIcon
from PyQt6.QtWidgets import QTableWidgetItem, QFileDialog, QDialog, QMessageBox

from src import Controller
from src.models import TimeRecord, HumanReadable
from humanfriendly import format_timespan
from codetiming import Timer


class MainWindowQt(QtWidgets.QMainWindow):
    pushButtonDeleteRecord = None
    tableByRecord = None
    pushButtonEdit = None
    editOpenedFile = None
    labelOvertimeSummary = None
    tableByMonth = None
    tableByDay = None

    def __init__(self, controller: Controller, version: str):
        # Call the inherited classes __init__ method
        super(MainWindowQt, self).__init__()

        # Load the .ui file
        uic.loadUi("src/MainWindow.ui", self)
        logging.info("Loaded main window...")
        self.setWindowTitle(f"Time Tracker V{version}")

        base_path = os.path.dirname(__file__)
        self.setWindowIcon(QIcon(os.path.join(base_path, "clock.png")))

        self.editOpenedFile.setAlignment(
            Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft
        )

        # init the controller
        self.__controller = controller
        self.__load_and_set_data(self.__controller.last_data_file)

        self.selected_raw_data = None

        self.show()
        # print(QColor.colorNames())

    @pyqtSlot(name="on_tableByRecord_itemSelectionChanged")
    def __by_record_item_changed(self):
        current_row = self.tableByRecord.currentRow()
        internal_id_widget = self.tableByRecord.item(current_row, 6)
        if internal_id_widget is not None:
            internal_id = int(internal_id_widget.text())
            found_data = filter(
                lambda _: _.internal_id == internal_id,
                self.__controller.time_analysis.raw_data,
            )
            self.selected_raw_data = next(found_data, None)
            self.pushButtonEdit.setEnabled(True)
            self.pushButtonDeleteRecord.setEnabled(True)
            logging.debug(
                f"Selected record with id {internal_id}: {str(self.selected_raw_data)}."
            )
        else:
            self.selected_raw_data = None
            self.pushButtonEdit.setEnabled(False)
            self.pushButtonDeleteRecord.setEnabled(False)
            logging.debug(f"Selected no record.")

    @pyqtSlot(name="on_pushButtonNewRecord_clicked")
    def __on_new_record(self):
        from datetime import datetime

        model = TimeRecord(
            internal_id=len(self.__controller.time_analysis.raw_data),
            start=datetime.now(),
            end=datetime.now(),
            all_overtime=False,
            comment=None,
        )

        if self.__show_edit_record_dialog(model):
            self.__controller.add_record(model, self.__controller.last_data_file)
            self.__set_data()

    @pyqtSlot(name="on_pushButtonEdit_clicked")
    def __on_edit_record(self):
        if self.__show_edit_record_dialog(self.selected_raw_data):
            self.__controller.record_has_been_updated()
            self.__set_data()

    @pyqtSlot(name="on_pushButtonDeleteRecord_clicked")
    def __on_delete_record(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Icon.Question)
        message_box.setText("Do you want to delete the record?")
        message_box.setStandardButtons(
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if message_box.exec() == QMessageBox.StandardButton.Yes:
            self.__controller.delete_record(self.selected_raw_data)
            self.__set_data()

    def __show_edit_record_dialog(self, model: TimeRecord) -> bool:
        from src.EditRecordDialog import EditRecordDialog

        logging.info(f"Shall edit record {model}...")
        dialog = EditRecordDialog(self, model)
        return dialog.exec() == QDialog.DialogCode.Accepted

    @pyqtSlot(name="on_buttonOpenFilePicker_clicked")
    def __select_file_via_picker(self):
        picker = QFileDialog(
            self, caption="Select data file", filter="Data files (*.csv)"
        )
        if picker.exec():
            file_name = picker.selectedFiles()[0]
            self.__load_and_set_data(file_name)

    def __load_and_set_data(self, file_name: str):
        self.__controller.load_data_file(file_name)
        self.__set_data()

    def __set_data(self):
        logging.info("setting data to ui...")
        self.editOpenedFile.setText(self.__controller.last_data_file)

        data = self.__controller.time_analysis

        total_overtime = HumanReadable.seconds_to_human_readable(
            data.get_total_overtime_seconds()
        )
        self.labelOvertimeSummary.setText(total_overtime)

        palette = QPalette()
        palette.setColor(
            QPalette.ColorRole.Text,
            MainWindowQt.__get_overtime_color(data.get_total_overtime_seconds()),
        )
        self.labelOvertimeSummary.setPalette(palette)

        # fill by month
        self.fill_table(
            self.tableByMonth,
            data.data_by_month,
            lambda scope: scope.scope_as_month(),
            "Month",
        )
        self.fill_table(
            self.tableByDay, data.data_by_day, lambda scope: scope.scope_as_day(), "Day"
        )
        self.fill_table_with_raw_data(self.tableByRecord, data.raw_data)

        logging.info("data successfully set to ui...")

    @staticmethod
    def __get_overtime_color(seconds: int) -> QColor:
        if seconds < 0:
            return QColor(255, 0, 0)
        else:
            return QColor(255, 255, 255) if seconds == 0 else QColor(0, 200, 0)

    @staticmethod
    def fill_table(table, data, scope_accessor, scope_label: str):
        with Timer(
            initial_text=f"fill_table({scope_label})",
            text=lambda secs: f"set data {scope_label} in {format_timespan(secs)}",
            logger=logging.info,
        ):
            table.setColumnCount(3)
            table.setHorizontalHeaderLabels([scope_label, "Hours", "Overtime"])

            table.setRowCount(len(data))
            for index, (item) in enumerate(
                sorted(data, key=lambda _: _.scope, reverse=True)
            ):
                item_scope = QTableWidgetItem()
                item_scope.setText(scope_accessor(item))
                item_worked = QTableWidgetItem()

                working_seconds = HumanReadable.seconds_to_human_readable(
                    item.working_seconds
                )
                working_decimal = HumanReadable.seconds_to_decimal_display(
                    item.working_seconds
                )
                item_worked.setText(f"{working_seconds} ({working_decimal})")
                item_worked.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                )

                item_overtime = QTableWidgetItem()
                item_overtime.setText(
                    HumanReadable.seconds_to_human_readable(item.overtime_seconds)
                )
                item_overtime.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )
                item_overtime.setForeground(
                    MainWindowQt.__get_overtime_color(item.overtime_seconds)
                )

                # item_color.setBackground(get_rgb_from_hex(code))
                table.setItem(index, 0, item_scope)
                table.setItem(index, 1, item_worked)
                table.setItem(index, 2, item_overtime)

            table.resizeColumnsToContents()

    @staticmethod
    def fill_table_with_raw_data(table, data):
        with Timer(
            initial_text=f"fill_table_with_raw_data()",
            text=lambda secs: f"fill_table_with_raw_data() set data in {format_timespan(secs)}",
            logger=logging.info,
        ):
            labels = ["Date", "Start", "End", "Duration", "Comment", "OT", "id"]
            table.setColumnCount(len(labels))
            table.setHorizontalHeaderLabels(labels)

            table.setRowCount(len(data))
            for index, (item) in enumerate(
                sorted(data, key=lambda _: _.start, reverse=True)
            ):
                item_scope = QTableWidgetItem()
                item_scope.setText(item.scope_as_day())

                item_start = QTableWidgetItem()
                item_start.setText(item.start.strftime("%H:%M"))

                item_end = QTableWidgetItem()
                item_end.setText(item.end.strftime("%H:%M"))

                item_duration = QTableWidgetItem()
                item_duration.setText(item.get_duration_display())
                item_duration.setTextAlignment(
                    Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                )

                item_comment = QTableWidgetItem()
                item_comment.setText(item.comment)
                item_comment.setTextAlignment(
                    Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
                )

                iten_all_overtime = QTableWidgetItem()
                iten_all_overtime.setText("Yes" if item.all_overtime else "No")
                iten_all_overtime.setTextAlignment(
                    Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter
                )

                item_internal_id = QTableWidgetItem()
                item_internal_id.setText(str(item.internal_id))

                table.setItem(index, 0, item_scope)
                table.setItem(index, 1, item_start)
                table.setItem(index, 2, item_end)
                table.setItem(index, 3, item_duration)
                table.setItem(index, 4, item_comment)
                table.setItem(index, 5, iten_all_overtime)
                table.setItem(index, 6, item_internal_id)

            table.resizeColumnsToContents()
