from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLabel
from database.database import get_filter_data
from services.services import get_income, get_unpaid_invoices, get_duplicate_invoices
from widgets.table_widget import Table


class AnalysisPage(QWidget):
    def __init__(self):
        super().__init__()

        self.analysis_layout = QGridLayout()
        self.setLayout(self.analysis_layout)

        self.table = Table()
        self.table.setSelectionMode(self.table.SelectionMode.NoSelection)

        self.income_button = QPushButton("Приход", clicked=self.income_info)
        self.income_label = QLabel()

        self.unpaid_invoices_button = QPushButton("Неплатени суми", clicked=self.unpaid_invoices_info)
        self.unpaid_invoices_label = QLabel()

        self.duplicates_button = QPushButton("Дублирани фактури", clicked=self.duplicate_invoices_info)
        self.duplicates_label = QLabel()

        self.show_button = QPushButton("Показване", clicked=self.show)
        self.home_button = QPushButton("Начало", clicked=self.refresh)

        self.analysis_layout.addWidget(self.income_button, 0, 0, 1, 1)
        self.analysis_layout.addWidget(self.income_label, 1, 0, 1, 1)
        self.analysis_layout.addWidget(self.unpaid_invoices_button, 0, 1, 1, 1)
        self.analysis_layout.addWidget(self.unpaid_invoices_label, 1, 1, 1, 1)
        self.analysis_layout.addWidget(self.duplicates_button, 0, 2, 1, 1)
        self.analysis_layout.addWidget(self.duplicates_label, 1, 2, 1, 1)
        self.analysis_layout.addWidget(self.home_button, 0, 3, 1, 1)
        self.analysis_layout.addWidget(self.show_button, 1, 3, 1, 1)
        self.analysis_layout.addWidget(self.table, 2, 0, 2, 4)

    def show(self) -> None:
        self.table.visualize_table()
        self.clear_labels()

    def refresh(self) -> None:
        self.table.clearContents()
        self.table.setRowCount(1)
        self.table.setVerticalHeaderLabels(["№"])

        self.clear_labels()

    def clear_labels(self) -> None:
        self.income_label.setText('')
        self.duplicates_label.setText('')
        self.unpaid_invoices_label.setText('')

    def income_info(self) -> None:
        result = get_income()
        message = ''

        if result:
            message = f"Общият приход е {result:.2f}."
            self.table.visualize_table()
        else:
            message = "В базата данни няма записи все още."

        self.income_label.setText(message)
        self.duplicates_label.setText('')
        self.unpaid_invoices_label.setText('')

    def unpaid_invoices_info(self) -> None:
        attribute = 'Платено'
        requirement = 'Не'
        info = get_filter_data(attribute, requirement)
        message = ''

        if info:
            message = f"Общата сума от неплатените суми е {get_unpaid_invoices():.2f}."
            self.table.visualize_table(info)
        else:
            message = f"Няма неплатени суми."
            self.table.setRowCount(1)

        self.unpaid_invoices_label.setText(message)
        self.income_label.setText('')
        self.duplicates_label.setText('')

    def duplicate_invoices_info(self) -> None:
        duplicate_invoices = get_duplicate_invoices()

        if duplicate_invoices:
            self.table.visualize_table(duplicate_invoices)
            self.duplicates_label.clear()
        else:
            self.duplicates_label.setText(f'Няма дублирани фактури.')
            self.table.setRowCount(1)

        self.income_label.setText('')
        self.unpaid_invoices_label.setText('')
