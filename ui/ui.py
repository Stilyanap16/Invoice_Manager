from PyQt6.QtWidgets import QMainWindow, QStackedWidget
from ui.home_page import HomePage
from ui.visual_page import VisualPage
from ui.analysis_page import AnalysisPage
from ui.charts_page import ChartsPage


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Invoice manager")
        self.resize(1000, 800)

        self.all_windows = QStackedWidget()

        self.home_page = HomePage()
        self.visual_page = VisualPage()
        self.analysis_page = AnalysisPage()
        self.charts_page = ChartsPage()

        self.all_windows.addWidget(self.home_page)
        self.all_windows.addWidget(self.visual_page)
        self.all_windows.addWidget(self.analysis_page)
        self.all_windows.addWidget(self.charts_page)
        self.setCentralWidget(self.all_windows)

        self.home_page.visual_button.clicked.connect(lambda: self.all_windows.setCurrentWidget(self.visual_page))
        self.home_page.analysis_button.clicked.connect(lambda: self.all_windows.setCurrentWidget(self.analysis_page))
        self.home_page.charts_button.clicked.connect(lambda: self.all_windows.setCurrentWidget(self.charts_page))

        self.visual_page.home_button.clicked.connect(lambda: self.all_windows.setCurrentWidget(self.home_page))
        self.analysis_page.home_button.clicked.connect(lambda: self.all_windows.setCurrentWidget(self.home_page))
        self.charts_page.home_button.clicked.connect(lambda: self.all_windows.setCurrentWidget(self.home_page))
