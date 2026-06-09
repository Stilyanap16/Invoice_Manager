from PyQt6.QtWidgets import QApplication
import sys
from database.database import create_database_and_table
from ui.ui import MainWindow


def main():
    app = QApplication(sys.argv)
    with open("styles/styles.qss", "r") as f:
        _style = f.read()
        app.setStyleSheet(_style)

    create_database_and_table()
    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
