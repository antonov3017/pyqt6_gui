from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
import sys


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(200, 200, 700, 400)
        self.setWindowTitle("Advance Styling")

        vbox = QVBoxLayout()

        label = QLabel("Enter Your Name :")
        vbox.addWidget(label)

        line = QLineEdit()
        vbox.addWidget(line)

        button = QPushButton("Submit")
        vbox.addWidget(button)

        self.setLayout(vbox)

        self.setStyleSheet("""
            QWidget {
                background-color:#f0f0f0;

            }

            QLabel {
                color:#333;
                font-size:18px;
                font-weight:bold


            }

            QLineEdit {
                padding:6px;
                border:2px solid #aaa;
                border-radius: 5px;

            }

            QPushButton {
                padding: 8px 16px;
                background-color: #4CAF50;
                color:white;
                font-size: 18px;
                border:none;
                border-radius: 5px;


            }


            QPushButton:hover {
                background-color: #45a049;



            }


             QPushButton:pressed {
                background-color: #367c39;



            }


        """)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())