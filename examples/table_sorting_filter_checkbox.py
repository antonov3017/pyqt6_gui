from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QCheckBox, QHBoxLayout
import sys
from PyQt6.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Sorting & Filtering")

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        self.filter_edit = QLineEdit()

        vbox = QVBoxLayout()
        vbox.addWidget(self.filter_edit)
        vbox.addWidget(self.table_widget)

        main_widget = QWidget()
        main_widget.setLayout(vbox)
        self.setCentralWidget(main_widget)

        self.setup_table()
        self.setup_connections()

    def setup_table(self):
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Category", "Price", "Date", "Check"])

        data = [
            ("Product 1", "Category A", "10", "2023-05-15", True),
            ("Product 2", "Category B", "15", "2023-06-10", False),
            ("Product 3", "Category A", "20", "2023-07-20", True),
            ("Product 4", "Category C", "25", "2023-08-05", False),
            ("Product 5", "Category B", "30", "2023-09-15", True)
        ]

        self.table_widget.setRowCount(len(data))

        for row, (name, category, price, date, checked) in enumerate(data):
            self.table_widget.setItem(row, 0, QTableWidgetItem(name))
            self.table_widget.setItem(row, 1, QTableWidgetItem(category))
            self.table_widget.setItem(row, 2, QTableWidgetItem(price))
            self.table_widget.setItem(row, 3, QTableWidgetItem(date))

            # Создание чекбокса и добавление его в колонку "Check"
            checkbox = QCheckBox()
            checkbox.setChecked(checked)

            # Центрируем чекбокс в ячейке
            central_widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)  # Убираем отступы
            central_widget.setLayout(layout)

            # Устанавливаем QWidget в ячейку
            self.table_widget.setCellWidget(row, 4, central_widget)

    def setup_connections(self):
        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.filter_edit.textChanged.connect(self.filter_table)

    def sort_table(self, column):
        self.table_widget.sortItems(column, Qt.SortOrder.AscendingOrder)

    def filter_table(self, filter_text):
        for row in range(self.table_widget.rowCount()):
            match = False
            for col in range(self.table_widget.columnCount() - 1):  # -1 чтобы не проверять колонку с чекбоксами
                item = self.table_widget.item(row, col)
                if item and filter_text.lower() in item.text().lower():
                    match = True
                    break
            self.table_widget.setRowHidden(row, not match)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())
