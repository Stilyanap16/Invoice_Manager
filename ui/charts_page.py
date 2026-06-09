from PyQt6.QtWidgets import QWidget, QPushButton, QGridLayout
from widgets.chart_widgets import BarChart, PieChart, LineChart
from database.database import get_data


class ChartsPage(QWidget):
    def __init__(self):
        super().__init__()

        self.charts_layout = QGridLayout()
        self.setLayout(self.charts_layout)

        self.home_button = QPushButton("Начало", clicked=self.refresh)

        self.bar_chart = BarChart()
        self.pie_chart = PieChart()
        self.line_chart = LineChart()

        self.show_button = QPushButton("Показване", clicked=self.show)

        self.charts_layout.addWidget(self.home_button, 0, 0, 1, 2)
        self.charts_layout.addWidget(self.show_button, 0, 2, 1, 2)
        self.charts_layout.addWidget(self.bar_chart, 1, 0, 2, 2)
        self.charts_layout.addWidget(self.line_chart, 1, 2, 1, 2)
        self.charts_layout.addWidget(self.pie_chart, 2, 2, 1, 2)


    def refresh(self) -> None:
        self.bar_chart.close()
        self.pie_chart.close()
        self.line_chart.close()

    def show(self) -> None:
        data = get_data()
        if data:
            self.bar_chart.visualize_chart()
            self.pie_chart.visualize_chart()
            self.line_chart.visualize_chart()
