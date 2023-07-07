from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem

from src import TimeAnalysis


class MainWindowQt(QtWidgets.QMainWindow):
    def __init__(self):
        # Call the inherited classes __init__ method
        super(MainWindowQt, self).__init__()
        # Load the .ui file
        uic.loadUi('src/MainWindow.ui', self)

        # configure tab view by month
        self.tableByMonth.setColumnCount(2)
        self.tableByMonth.setHorizontalHeaderLabels(["Month", "Hours"])

        # Set the label text
        # self.mainLabel.setText("Updated Text")
        # Show the widget
        self.show()

    def set_data(self, data : TimeAnalysis):
        total_overtime = '{:.2f}'.format(data.get_total_overtime_seconds() / 60 / 60)

        self.labelOvertimeSummary.setText(total_overtime)

        # fill by month
        self.tableByMonth.setRowCount(len(data.data_by_month))
        for index, (item) in enumerate(data.data_by_month):
            item_name = QTableWidgetItem()
            item_name.setText(item.scope.strftime('%m.%Y'))
            item_code = QTableWidgetItem()
            item_code.setText('{:.2f}'.format(item.overtime_seconds / 60 / 60))

            # item_color.setBackground(get_rgb_from_hex(code))
            self.tableByMonth.setItem(index, 0, item_name)
            self.tableByMonth.setItem(index, 1, item_code)
