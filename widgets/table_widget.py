from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem
from database.database import get_column_names, get_data, make_record_readable


class Table(QTableWidget):
    def __init__(self):
        super().__init__()

        self.column_names = get_column_names()
        self.number_of_columns = len(self.column_names)

        self.setColumnCount(self.number_of_columns)
        self.setRowCount(1)

        self.setHorizontalHeaderLabels(self.column_names)
        self.setVerticalHeaderLabels(["№"])

    def visualize_table(self, info=None) -> None:
        data = info if info else get_data()
        if data:
            number_of_rows = len(data)
            self.setRowCount(number_of_rows + 1)

            row_nums = ["№"] + [str(i) for i in range(1, number_of_rows + 1)]
            self.setVerticalHeaderLabels(row_nums)

            for row in range(number_of_rows):
                record = list(data[row])
                if record[0]:
                    record = make_record_readable(record)
                    record[4] = f"{record[4]:.2f}"
                    record[5] = f"{record[5]:.2f}"

                for col, value in enumerate(record):
                    table_item = QTableWidgetItem(value)
                    table_item.setFlags(table_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
                    self.setItem(row + 1, col, table_item)

            self.horizontalHeader().setStretchLastSection(True)
