from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView
import sys
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QIcon

class TreeViewWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200,200, 700, 400)
        self.setWindowTitle("PyQt6 QTreeView")

        self.tree_view = QTreeView()
        self.setCentralWidget(self.tree_view)

        self.model = QStandardItemModel()
        self.tree_view.setModel(self.model)

        self.file_explorer()


    def file_explorer(self):
        root_item = QStandardItem("Root")
        self.model.appendRow(root_item)

        folder_item = QStandardItem("Folder 1")
        file_item = QStandardItem("File 1")
        file_item.setIcon(QIcon("python.png"))
        file_item.setToolTip("This is file 1")
        root_item.appendRow(folder_item)
        folder_item.appendRow(file_item)

app = QApplication(sys.argv)
window = TreeViewWindow()
window.show()
sys.exit(app.exec())


