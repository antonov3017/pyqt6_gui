from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView
import sys
from PyQt6.QtGui import QStandardItem, QStandardItemModel, QIcon
from PyQt6.QtCore import Qt


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

        self.tree_view.setDragEnabled(True)
        self.tree_view.setAcceptDrops(True)
        self.tree_view.setDropIndicatorShown(True)


    def file_explorer(self):
        root_item = QStandardItem("Root")
        self.model.appendRow(root_item)

        folder_item = QStandardItem("Folder 1")
        file_item = QStandardItem("File 1")
        file_item.setIcon(QIcon("python.png"))
        file_item.setToolTip("This is file 1")
        root_item.appendRow(folder_item)
        folder_item.appendRow(file_item)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropActions(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            event.setDropActions(Qt.DropAction.MoveAction)
            event.accept()
        else:
            event.ignore()



app = QApplication(sys.argv)
window = TreeViewWindow()
window.show()
sys.exit(app.exec())


