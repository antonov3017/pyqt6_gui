import sys
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QTableView, QHeaderView, QVBoxLayout, QWidget
from PyQt6.QtGui import QStandardItem, QStandardItemModel


class ExampleApp(QWidget):
    def __init__(self):
        super().__init__()

        # Create the model
        self.model = QStandardItemModel(4, 2)  # 4 rows and 2 columns
        self.setWindowTitle("QTableView with Centered CheckBoxes")

        # Set horizontal headers
        self.model.setHorizontalHeaderLabels(['Column 1', 'Column 2'])

        # Add checkboxes to the model
        for row in range(4):
            # Создание элемента и установка его как чекбокс
            checkBoxItem = QStandardItem()
            checkBoxItem.setCheckable(True)
            checkBoxItem.setCheckState(Qt.CheckState.Unchecked)  # Изначальное состояние - не отмечен

            # Установка текста чекбокса пустым
            checkBoxItem.setText("")  # Оставляем текст пустым

            # Центрируем чекбокс по горизонтали и вертикали
            checkBoxItem.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

            # Add the checkbox item to the model
            self.model.setItem(row, 0, checkBoxItem)

            # Create a QStandardItem for the second column
            item = QStandardItem(f"Row {row + 1}, Column 2")
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
            self.model.setItem(row, 1, item)

        # Create the table view
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Center the headers
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.table_view)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExampleApp()
    window.resize(400, 300)  # Set window size
    window.show()
    sys.exit(app.exec())
