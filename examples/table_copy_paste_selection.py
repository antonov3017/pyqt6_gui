from PyQt6.QtWidgets import QApplication,QMainWindow,QTableWidget, QMenu, QTableWidgetItem
import sys
from PyQt6.QtGui import QAction, QKeySequence
from PyQt6.QtCore import Qt, QMimeData


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200,200, 700, 400)
        self.setWindowTitle("Clipboard Operations")

        self.table_widget = QTableWidget()
        self.setCentralWidget(self.table_widget)


        self.setup_table()




    def setup_table(self):
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Name", "Age", "Email"])

        data = [
            ("John", "25", "john@example.com"),
            ("Alice", "32", "alice@example.com"),
            ("Bob", "40", "bob@example.com")
        ]

        self.table_widget.setRowCount(len(data))

        for row, (name, age, email) in enumerate(data):
            name_item = QTableWidgetItem(name)
            self.table_widget.setItem(row, 0, name_item)

            age_item = QTableWidgetItem(age)
            self.table_widget.setItem(row, 1, age_item)

            email_item = QTableWidgetItem(email)
            self.table_widget.setItem(row, 2, email_item)

        self.table_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.ActionsContextMenu)
        self.create_context_menu_actions()
        self.table_widget.addAction(self.copy_action)
        self.table_widget.addAction(self.paste_action)


    def create_context_menu_actions(self):
        self.copy_action = QAction("Copy", self)
        self.copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        self.copy_action.triggered.connect(self.copy_selected_cell)

        self.paste_action = QAction("Paste", self)
        self.paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        self.paste_action.triggered.connect(self.paste_selected_cell)



    def copy_selected_cell(self):
        selection = self.table_widget.selectedRanges()
        if not selection:
            return
        cells_text = []

        for selection_range in selection:
            for row in range(selection_range.topRow(), selection_range.bottomRow() + 1):
                for column in range(selection_range.leftColumn(), selection_range.rightColumn() + 1):
                    item = self.table_widget.item(row, column)
                    if item:
                        cells_text.append(item.text())

        mime_data = QMimeData()
        mime_data.setText('\t'.join(cells_text))
        clipboard = QApplication.clipboard()
        clipboard.setMimeData(mime_data)


    def paste_selected_cell(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()

        if mime_data.hasText():
            text = mime_data.text()
            cells_text = text.split('\t')

            current_range = self.table_widget.selectedRanges()[0]

            top_row = current_range.topRow()
            left_column = current_range.leftColumn()

            for row in range(current_range.rowCount()):
                for column in range(current_range.columnCount()):
                    item = self.table_widget.item(top_row+ row, left_column + column)

                    if item:
                        if cells_text:
                            item.setText(cells_text.pop(0))
                        else:
                            return

    def contextMenuEvent(self, event):
        context_menu = QMenu()
        context_menu.addAction(self.copy_action)
        context_menu.addAction(self.paste_action)
        context_menu.exec(event.globalPos())



app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())