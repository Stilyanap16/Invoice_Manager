from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit, QLabel
from services.import_and_export import import_from_excel, export_to_excel


class HomePage(QWidget):
    def __init__(self):
        super().__init__()

        self.home_layout = QGridLayout()
        self.setLayout(self.home_layout)

        self.file_path_field = QLineEdit()
        self.file_path_field.setPlaceholderText("Въведете пътя до Excel файла:")

        self.import_button = QPushButton("Импортиране", clicked=self.import_info)

        self.export_button = QPushButton("Експортиране", clicked=self.export_info)

        self.export_status_label = QLabel()

        self.visual_button = QPushButton("Визуализация", clicked=self.export_status_label.clear)

        self.analysis_button = QPushButton("Анализ", clicked=self.export_status_label.clear)

        self.charts_button = QPushButton("Графики", clicked=self.export_status_label.clear)

        self.home_layout.addWidget(self.import_button, 0, 0, 5, 1)
        self.home_layout.addWidget(self.file_path_field, 1, 0, 5, 3)
        self.home_layout.addWidget(self.export_button, 0, 2, 5, 1)
        self.home_layout.addWidget(self.export_status_label, 0, 1, 1, 1)
        self.home_layout.addWidget(self.visual_button, 4, 1, 5, 1)
        self.home_layout.addWidget(self.analysis_button, 3, 0, 5, 1)
        self.home_layout.addWidget(self.charts_button, 5, 2, 5, 1)

    def import_info(self) -> None:
        file_path = self.file_path_field.text()
        status_text = import_from_excel(file_path)
        self.file_path_field.setText(status_text)
        self.export_status_label.clear()

    def export_info(self) -> None:
        status_text = export_to_excel()
        self.export_status_label.setText(status_text)
