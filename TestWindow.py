from TestMenu import TestMenu

from Picture_Player1 import Picture_Player1
from Big_Field import Big_Field
from Canva import Canva

from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setGeometry(0, 0, 1920, 1080)

        self.central_widget = QWidget()
        self.layout = QHBoxLayout(self.central_widget)

        self.player1 = Picture_Player1(self.central_widget)
        self.player2 = Picture_Player1(self.central_widget)

        self.layout.addWidget(self.player1)
        self.createCanvas()
        self.big_field = Big_Field(self.central_widget, self.canvas)
        self.layout.addWidget(self.big_field)
        self.layout.addWidget(self.player2)

        self.big_field.set_player_names(self.player1.get_name(), self.player2.get_name())
        self.player1.button_player_name.textChanged.connect(self.update_player_names)
        self.player2.button_player_name.textChanged.connect(self.update_player_names)

        self.menuBar = TestMenu(self)
        self.setMenuBar(self.menuBar)
        self.menuBar.saveMenuAction.triggered.connect(self.menuBar.save)
        self.menuBar.loadMenuAction.triggered.connect(self.menuBar.load)

        self.setCentralWidget(self.central_widget)

    def update_player_names(self):
        self.big_field.set_player_names(self.player1.get_name(), self.player2.get_name())


    def createCanvas(self):
        self.canvas = Canva(self)
        self.canvas.setGeometry(605, 187, 740, 740)
        self.canvalayout = QVBoxLayout()
        self.canvalayout.addWidget(self.canvas)