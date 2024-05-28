from PyQt6.QtWidgets import QWidget, QPushButton, QFileDialog, QLabel
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtWidgets import QGridLayout, QLineEdit

class Picture_Player1(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setFixedSize(450, 400)

        self.layout = QGridLayout(self)
        self.layout.setHorizontalSpacing(300)

        self.picture = QLabel()
        self.layout.addWidget(self.picture, 0, 0)

        self.button = QPushButton("Open Image")
        self.button.setFont(QFont("Arial", 15))
        self.layout.addWidget(self.button, 1, 0)
        self.button.clicked.connect(self.showImage)

        self.button_player_name = QLineEdit()
        self.button_player_name.setPlaceholderText("Enter player name")
        self.button_player_name.setFont(QFont("Arial", 15))
        self.layout.addWidget(self.button_player_name, 2, 0)

    def get_name(self):
        return self.button_player_name.text()

    def showImage(self):
        file = QFileDialog(self)
        fileName = file.getOpenFileName()[0]
        pixmap = QPixmap(fileName)
        pixmap = pixmap.scaled(450, 250)
        self.picture.setPixmap(pixmap)

    def openImage(self):
        pixmap = QPixmap(self.input.displayText())
        pixmap = pixmap.scaled(450, 200)
        self.picture.setPixmap(pixmap)