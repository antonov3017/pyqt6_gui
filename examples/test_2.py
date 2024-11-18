from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QVBoxLayout, \
    QCheckBox, QHBoxLayout, QPushButton
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
        self.table_widget.setColumnCount(6)  # Добавили дополнительный столбец для кнопок сворачивания
        self.table_widget.setHorizontalHeaderLabels(["Toggle", "Name", "Category", "Sort", "Shelf", "Check"])

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
            ("Product 3", "Category A", "Sort1", "2C", True, [
                (1, 100, '2024-10-02', 'Remarks 1'),
                (3, 400, '2024-11-02', 'Remarks 2'),
                (3, 400, '2024-11-02', 'Remarks 2'),
                (2, 700, '2024-10-22', 'Remarks 3'),
            ]),
            ("Product 4", "Category C", "Sort3", "2D", False, [
                (1, 534, '2024-10-02', 'Remarks 1'),
            ]),
            ("Product 5", "Category B", "Sort1", "2A", True, None)
        ]

        row_index = 0

        for name, category, sort_, shelf, checked, details in data:
            # Основная строка
            self.table_widget.insertRow(row_index)

            toggle_button = QPushButton('▼')
            toggle_button.clicked.connect(lambda _, row=row_index: self.toggle_details(row))
            self.table_widget.setCellWidget(row_index, 0, toggle_button)

            self.table_widget.setItem(row_index, 1, QTableWidgetItem(name))
            self.table_widget.setItem(row_index, 2, QTableWidgetItem(category))
            self.table_widget.setItem(row_index, 3, QTableWidgetItem(sort_))
            self.table_widget.setItem(row_index, 4, QTableWidgetItem(shelf))

            checkbox = QCheckBox()
            checkbox.setChecked(checked)
            central_widget = QWidget()
            layout = QHBoxLayout()
            layout.addWidget(checkbox)
            layout.setContentsMargins(0, 0, 0, 0)
            central_widget.setLayout(layout)
            self.table_widget.setCellWidget(row_index, 5, central_widget)

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

                nested_table.updateGeometry()

                row_for_details = row_index + 1
                toggle_button.details_row = row_for_details

                height = max(nested_table.sizeHintForRow(i) for i in range(
                    nested_table.rowCount())) * nested_table.rowCount() + nested_table.horizontalHeader().height()

                # Устанавливаем высоту строки для отображения всего контента
                print(f'Adjusting height for row {row_for_details} to {height}.')

                self.table_widget.insertRow(row_for_details)
                self.table_widget.setRowHeight(row_index + 1, height)

                nested_table.hide()

                toggle_button.nested_table = nested_table
                span_count = len(
                    self.table_widget.horizontalHeader())  # количество коллонок для объединения ячеек во вложенной таблице

                self.table_widget.setSpan(toggle_button.details_row, 0, 1, span_count)

                self.table_widget.setCellWidget(toggle_button.details_row, 0, nested_table)

                # Увеличение индекса строки
            row_index += 2 if details else +1

    def toggle_details(self, row):
        # Получаем виджет кнопки из текущей строки
        toggle_button = self.table_widget.cellWidget(row, 0)

        # Проверяем, существует ли строка с деталями
        if hasattr(toggle_button, 'details_row'):
            details_row = toggle_button.details_row

            # Изменяем видимость вложенной таблицы
            nested_table = self.table_widget.cellWidget(details_row, 0)

            if nested_table.isVisible():
                nested_table.hide()
                toggle_button.setText('►')  # Меняем текст кнопки на стрелку вправо (раскрыть)
                self.table_widget.setRowHeight(row + 1, 0)
            else:
                nested_table.show()
                toggle_button.setText('▼')  # Меняем текст кнопки на стрелку вниз (свернуть)

    # Подключение остальных методов сортировки и фильтрации

    def setup_connections(self):
        self.table_widget.horizontalHeader().sectionClicked.connect(self.sort_table)
        self.filter_edit.textChanged.connect(self.filter_table)

    def sort_table(self, column):
        self.table_widget.sortItems(column + 1, Qt.SortOrder.AscendingOrder)  # Смещение на один столбец справа

    def filter_table(self, filter_text):
        for row in range(0, self.table_widget.rowCount(), 2):  # Проходим только по основным строкам
            match = False
            for col in range(1, self.table_widget.columnCount() - 1):  # Пропускаем колонку с кнопкой и чекбоксами
                item = self.table_widget.item(row, col)
                if item and filter_text.lower() in item.text().lower():
                    match = True
                    break
            details_row = row + 1
            self.table_widget.setRowHidden(row, not match)
            self.table_widget.setRowHidden(details_row,
                                           not match or not self.table_widget.cellWidget(details_row, 0).isVisible())

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())

