from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from services.services import get_incomes_by_categories, get_percent_of_paid_and_unpaid_invoices, get_income_by_months


class Chart(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        self.layout.addWidget(self.canvas)

class BarChart(Chart):
    def __init__(self):
        super().__init__()

    def visualize_chart(self) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)

        ax.tick_params(axis="x", rotation=90)
        ax.set_title("Приход по категории")
        ax.set_xlabel("Категории")
        ax.set_ylabel("Приход")

        categories, values = get_incomes_by_categories()
        ax.bar(categories, values)

        self.figure.tight_layout()
        self.canvas.draw()
        self.show()

class PieChart(Chart):
    def __init__(self):
        super().__init__()

    def visualize_chart(self) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Процент платени фактури")
        ax.axis("equal")

        pie_chart_data = get_percent_of_paid_and_unpaid_invoices()
        ax.pie(pie_chart_data, labels=['Да', 'Не'], autopct="%1.2f%%", startangle=90)

        self.figure.tight_layout()
        self.canvas.draw()
        self.show()

class LineChart(Chart):
    def __init__(self):
        super().__init__()

    def visualize_chart(self) -> None:
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_title("Приход по месеци")
        ax.set_xlabel("Месеци")
        ax.set_ylabel("Приход")

        months, values = get_income_by_months()
        ax.plot(months, values)

        self.figure.tight_layout()
        self.canvas.draw()
        self.show()
