import os.path

from PyQt6.QtWidgets import QApplication, QMainWindow, QTreeView, QWidget,QVBoxLayout
from PyQt6.QtCore import Qt, QFileSystemWatcher, QModelIndex
from PyQt6.QtGui import QFileSystemModel
import sys


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(200,200, 700, 400)
        self.setWindowTitle("QTreeView Dynamic Updates")

        self.tree_view = QTreeView()


        self.model = QFileSystemModel()
        self.model.setRootPath("")
        self.tree_view.setModel(self.model)

        layout = QVBoxLayout()
        layout.addWidget(self.tree_view)

        main_widget = QWidget()
        main_widget.setLayout(layout)
        self.setCentralWidget(main_widget)

        self.setup_file_watcher()


    def setup_file_watcher(self):
        self.file_watcher = QFileSystemWatcher()
        self.file_watcher.directoryChanged.connect(self.handle_directory)
        self.file_watcher.fileChanged.connect(self.file_changed)


    def handle_directory(self, directory):
        index = self.model.index(directory)
        self.tree_view.update(index)


    def file_changed(self, file):
        directory = os.path.dirname(file)
        index = self.model.index(directory)
        self.tree_view.update(index)

    def add_directory_to_watch(self, directory):
        self.file_watcher.addPath(directory)

app = QApplication(sys.argv)
window = Window()
window.add_directory_to_watch(os.getcwd())
window.show()
sys.exit(app.exec())


