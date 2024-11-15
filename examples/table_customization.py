from PyQt6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("QTableWidget Customization")

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)

        self.setup_table()

    def setup_table(self):
        self.table_widget.setColumnCount(3)
        self.table_widget.setRowCount(5)

        for row in range(self.table_widget.rowCount()):
            for col in range(self.table_widget.columnCount()):
                item = QTableWidgetItem(f"Row {row + 1}, Column {col + 1}")
                self.table_widget.setItem(row, col, item)

        self.table_widget.setStyleSheet(

            """
            QTableWidget {
                background-color:#F5F5F5;
                font-family:Arial;
                border:1px solid black;


            }

            QTableWidget::item {
                border-bottom: 1px solid black;
                padding:5px;


            }


             QTableWidget::item:selected {
                background-color:#A9D9F7

             }

              QTableWidget::item:selected:!active {
                color:black

             }


            """
        )


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())