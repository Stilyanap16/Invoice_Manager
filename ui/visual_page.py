from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout, QLineEdit, QComboBox, QMessageBox, QLabel
from database.database import get_column_names, edit_data, delete_data, get_filter_data
from widgets.table_widget import Table


class VisualPage(QWidget):
    def __init__(self):
        super().__init__()

        self.visual_layout = QGridLayout()
        self.setLayout(self.visual_layout)

        self.edit_popup = EditPopup()
        self.edit_popup.save_button.clicked.connect(lambda: self.edit_info())
        self.edit_popup.cancel_button.clicked.connect(lambda: self.setEnabled(True))

        self.table = Table()

        self.show_button = QPushButton("Показване", clicked=self.table.visualize_table)

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Въведете по какво да се търси:")

        self.search_button = QPushButton("Търсене", clicked=self.search_table)

        self.attribute_list = QComboBox()
        self.attribute_list.addItems(get_column_names())

        self.requirement_field = QLineEdit()
        self.requirement_field.setPlaceholderText("Въведете по какво да се филтрира:")

        self.home_button = QPushButton("Начало", clicked=self.refresh)

        self.delete_button = QPushButton("Изтриване", clicked=self.delete_dialog, enabled=False)

        self.edit_button = QPushButton("Редактиране", clicked=self.edit_popup.show, enabled=False)
        self.edit_button.clicked.connect(lambda: self.setEnabled(False))

        self.filter_button = QPushButton("Филтриране", clicked=self.filter_info)

        self.refresh_button = QPushButton("Обновяване", clicked=self.refresh)


        self.visual_layout.addWidget(self.refresh_button, 0, 0, 1, 1)
        self.visual_layout.addWidget(self.search_button, 0, 1, 1, 1)
        self.visual_layout.addWidget(self.search_field, 0, 2, 1, 1)
        self.visual_layout.addWidget(self.show_button, 0, 3, 1, 1)
        self.visual_layout.addWidget(self.home_button, 0, 4, 1, 1)
        self.visual_layout.addWidget(self.table, 2, 0, 2, 5)
        self.visual_layout.addWidget(self.filter_button, 1, 0, 1, 1)
        self.visual_layout.addWidget(self.attribute_list, 1, 1, 1, 1)
        self.visual_layout.addWidget(self.requirement_field, 1, 2, 1, 1)
        self.visual_layout.addWidget(self.edit_button, 1, 3, 1, 1)
        self.visual_layout.addWidget(self.delete_button, 1, 4, 1, 1)

    def search_table(self) -> None:
        search_text = self.search_field.text()
        if search_text and self.table.rowCount() != 0:
            self.table.setCurrentItem(None)

            needed_cells = self.table.findItems(search_text, Qt.MatchFlag.MatchContains)

            if needed_cells:
                for cell in needed_cells:
                    cell.setSelected(True)
                self.table.setFocus()
            else:
                self.search_field.setText("Няма намерени резултати.")

    def filter_info(self) -> None:
        attribute = self.attribute_list.currentText()
        requirement = self.requirement_field.text()
        if requirement:
            info = get_filter_data(attribute, requirement)
            if info:
                self.table.visualize_table(info)
                self.edit_button.setEnabled(True)
                self.delete_button.setEnabled(True)
                self.show_button.setEnabled(False)
                self.requirement_field.setEnabled(False)
                self.attribute_list.setEnabled(False)
            else:
                self.table.setRowCount(1)

    def edit_info(self):
        attribute = self.attribute_list.currentText()
        requirement = self.requirement_field.text()
        second_attribute = self.edit_popup.needed_attribute_list.currentText()
        value = self.edit_popup.value_field.text()
        if value:
            result = edit_data(attribute, requirement, second_attribute, value)
            if result:
                self.edit_popup.value_field.setText(result)
            else:
                self.edit_popup.reset()
                self.setEnabled(True)
                self.refresh()

    def delete_dialog(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Предупреждение")
        dialog.setText("Сигурни ли сте, че искате да изтриете тези записи?")
        save_btn = dialog.addButton("Запазване", QMessageBox.ButtonRole.AcceptRole)
        dialog.addButton("Отказ", QMessageBox.ButtonRole.RejectRole)

        dialog.setIcon(QMessageBox.Icon.Warning)
        dialog.exec()
        button = dialog.clickedButton()

        if button == save_btn:
            self.delete_info()
        else:
            dialog.close()

    def delete_info(self) -> None:
        attribute = self.attribute_list.currentText()
        requirement = self.requirement_field.text()
        delete_data(attribute, requirement)
        self.refresh()
        self.table.visualize_table()

    def refresh(self) -> None:
        self.show_button.setEnabled(True)
        self.requirement_field.setEnabled(True)
        self.attribute_list.setEnabled(True)

        self.edit_button.setEnabled(False)
        self.delete_button.setEnabled(False)

        self.search_field.setText("")
        self.requirement_field.setText("")

        self.table.clearContents()
        self.table.setRowCount(1)
        self.table.setVerticalHeaderLabels(["№"])

class EditPopup(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Edit")
        self.resize(400, 200)

        self.edit_layout = QGridLayout()
        self.setLayout(self.edit_layout)

        self.instruction_label = QLabel("Изберете поле за редактиране и въведете нова стойнист.")

        self.needed_attribute_list = QComboBox()
        self.needed_attribute_list.addItems(get_column_names()[1:])

        self.value_field = QLineEdit()
        self.value_field.setPlaceholderText("Въведете стойност:")

        self.save_button = QPushButton("Запазване")
        self.cancel_button = QPushButton("Отказ", clicked=self.reset)

        self.edit_layout.addWidget(self.instruction_label, 0, 0, 1, 2)
        self.edit_layout.addWidget(self.needed_attribute_list, 1, 0, 1, 1)
        self.edit_layout.addWidget(self.value_field, 1, 1, 1, 1)
        self.edit_layout.addWidget(self.save_button, 2, 0, 1, 1)
        self.edit_layout.addWidget(self.cancel_button, 2, 1, 1, 1)

    def reset(self) -> None:
        self.needed_attribute_list.setCurrentIndex(0)
        self.value_field.setText("")
        self.close()
