from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, QCheckBox, QHBoxLayout
import sys
from PyQt6.QtCore import Qt


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 800, 600)
        self.setWindowTitle("Nested Table Example")

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
        self.table_widget.setHorizontalHeaderLabels(["Name", "Category", "Sort", "Shelf", "Check"])

        data = [
            ("Product 1", "Category A", "Sort1", "2A", True, [
                (1, 100, '2024-10-02', 'Remarks 1'),
                (3, 400, '2024-11-02', 'Remarks 2'),
                (2, 700, '2024-10-22', 'Remarks 3'),
            ]),
            ("Product 2", "Category B", "Sort2", "2B", False, [
                (1, 34, '2024-10-02', 'Remarks 4'),
                (2, 66, '2024-10-22', 'Remarks 34'),
            ]),
            ("Product 3", "Category A", "Sort1", "2C", True, None),
            ("Product 4", "Category C", "Sort3", "2D", False, [
                (1, 534, '2024-10-02', 'Remarks 1'),
            ]),
            ("Product 5", "Category B", "Sort1", "2A", True, None)
        ]

        row_index = 0  # Начинаем с первой строки

        for name, category, sort_, shelf, checked, details in data:
            # Основная строка
            self.table_widget.insertRow(row_index)
            self.table_widget.setItem(row_index, 0, QTableWidgetItem(name))
            self.table_widget.setItem(row_index, 1, QTableWidgetItem(category))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(sort_))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(shelf))

            # Чекбокс
            checkbox = QCheckBox()
            checkbox.setChecked(checked)
            central_widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(checkbox, alignment=Qt.AlignmentFlag.AlignCenter)
            layout.setContentsMargins(0, 0, 0, 0)
            central_widget.setLayout(layout)
            self.table_widget.setCellWidget(row_index, 4, central_widget)

            # Создаем вложенный QTableWidget, если есть детали
            if details:
                nested_table = QTableWidget()
                nested_table.setColumnCount(4)
                nested_table.setHorizontalHeaderLabels(["ID", "Price", "Date", "Remarks"])
                nested_table.setRowCount(len(details))

                for detail_row, (id_, price, date, remarks) in enumerate(details):
                    nested_table.setItem(detail_row, 0, QTableWidgetItem(str(id_)))
                    nested_table.setItem(detail_row, 1, QTableWidgetItem(str(price)))
                    nested_table.setItem(detail_row, 2, QTableWidgetItem(date))
                    nested_table.setItem(detail_row, 3, QTableWidgetItem(remarks))

                # Принудительное обновление геометрии
                nested_table.updateGeometry()

                # Вставляем строку для вложенной таблицы
                self.table_widget.insertRow(row_index + 1)  # Вставляем новую строку для вложенной таблицы
                self.table_widget.setSpan(row_index + 1, 0, 1, 5)  # Объединяем ячейки в строке

                # Устанавливаем вложенную таблицу
                self.table_widget.setCellWidget(row_index + 1, 0, nested_table)

                # Устанавливаем высоту строки в зависимости от количества вложенных строк
                # height = nested_table.sizeHint().height() + 0  # можно добавить небольшой отступ
                height = (len(details) + 1) * 30
                print(f'{height=}')
                self.table_widget.setRowHeight(row_index + 1, height)

            row_index += 2 if details else 1  # Увеличиваем индекс строк на 2, если есть вложенные данные, иначе на 1

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
