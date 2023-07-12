import logging

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QTableWidgetItem, QFileDialog

from src import TimeAnalysis, Controller


class MainWindowQt(QtWidgets.QMainWindow):
    def __init__(self, controller: Controller):

        # Call the inherited classes __init__ method
        super(MainWindowQt, self).__init__()

        # Load the .ui file
        uic.loadUi('src/MainWindow.ui', self)
        logging.info('Loaded main window...')

        # init the controller
        self.__controller = controller
        self.__load_and_set_data(self.__controller.last_data_file)

        self.show()

    @pyqtSlot('int', name="on_tabData_currentChanged")
    def tab_current_changed(self, index: int):
        if index == 2:
            self.groupBoxRecordDetail.show()
        else:
            self.groupBoxRecordDetail.hide()

    @pyqtSlot(name="on_buttonOpenFilePicker_clicked")
    def select_file_via_picker(self):
        picker = QFileDialog(self, caption="Select data file", filter="Data files (*.csv)")
        if picker.exec_():
            file_name = picker.selectedFiles()[0]
            self.__load_and_set_data(file_name)

    def __load_and_set_data(self, file_name: str):
        self.__controller.load_data_file(file_name)
        self.__set_data()

    def __set_data(self):
        logging.info('setting data to ui...')
        self.editOpenedFile.setPlainText(self.__controller.last_data_file)

        data = self.__controller.time_analysis
        total_overtime = '{:.2f}'.format(data.get_total_overtime_hours())
        self.labelOvertimeSummary.setText(total_overtime)

        # fill by month
        self.fill_table(self.tableByMonth, data.data_by_month, lambda scope: scope.scope_as_month())
        self.fill_table(self.tableByDay, data.data_by_day, lambda scope: scope.scope_as_day())
        self.fill_table_with_raw_data(self.tableByRecord, data.raw_data)

        logging.info('data successfully set to ui...')

    @staticmethod
    def fill_table(table, data, scope_accessor):
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Month", "Hours", "Overtime"])

        table.setRowCount(len(data))
        for index, (item) in enumerate(sorted(data, key=lambda _: _.scope, reverse=True)):
            item_scope = QTableWidgetItem()
            item_scope.setText(scope_accessor(item))
            item_worked = QTableWidgetItem()
            item_worked.setText('{:.2f}'.format(item.working_hours()))
            item_overtime = QTableWidgetItem()
            item_overtime.setText('{:.2f}'.format(item.overtime_hours()))

            # item_color.setBackground(get_rgb_from_hex(code))
            table.setItem(index, 0, item_scope)
            table.setItem(index, 1, item_worked)
            table.setItem(index, 2, item_overtime)

            table.resizeColumnsToContents()

    @staticmethod
    def fill_table_with_raw_data(table, data):
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Date", "Start", "End", "Duration"])

        init_column_width=60
        table.setRowCount(len(data))
        for index, (item) in enumerate(sorted(data, key=lambda _: _.start, reverse=True)):
            item_scope = QTableWidgetItem()
            item_scope.setText(item.scope_as_day())

            item_start = QTableWidgetItem()
            item_start.setText(item.start.strftime('%H:%M'))

            item_end = QTableWidgetItem()
            item_end.setText(item.end.strftime('%H:%M'))

            item_duration = QTableWidgetItem()
            item_duration.setText(item.get_duration_display())

            # item_color.setBackground(get_rgb_from_hex(code))
            table.setItem(index, 0, item_scope)
            table.setItem(index, 1, item_start)
            table.setItem(index, 2, item_end)
            table.setItem(index, 3, item_duration)

            table.resizeColumnsToContents()
