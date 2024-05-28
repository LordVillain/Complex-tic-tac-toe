from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

class Small_Field(QWidget):
    move_made = pyqtSignal(str, int, int)
    right_move_made = pyqtSignal(int, int)

    def __init__(self, parent: QWidget, canva):
        super().__init__(parent)

        self.current_player = "X"
        self.block_value = ""
        self.canva = canva

        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.buttons = [["" for _ in range(3)] for _ in range(3)]

        mainLayout = QVBoxLayout(self)
        mainLayout.setSpacing(0)

        rowLayout = QHBoxLayout()
        rowLayout.setSpacing(0)

        gameField = QWidget()
        gameField.setFixedSize(250, 250)
        gameLayout = QGridLayout(gameField)

        for row in range(3):
            for col in range(3):
                button = QPushButton()
                button.setStyleSheet("color: transparent;")
                button.setStyleSheet("background-color: transparent;")
                font = QFont()
                font.setWeight(QFont.Weight.Bold)
                button.setFixedSize(77, 77)
                self.set_font(button)
                button.clicked.connect(lambda _, r=row, c=col: self.button_clicked(r, c))
                gameLayout.addWidget(button, row, col)
                self.buttons[row][col] = button

        rowLayout.addWidget(gameField)
        mainLayout.addLayout(rowLayout)

    def set_font(self, button):
        font = QFont("Arial", 16)
        font.setBold(True)
        button.setFont(font)


    def button_clicked(self, row, col):
        which_button = self.sender()
        if which_button.text():
            return
        
        self.board[row][col] = self.current_player

        if self.check_winner_in_block(self.current_player):
            self.show_single_button(self.current_player)
        
        elif self.check_draw_in_block():
            self.show_single_button("D")
            
        self.right_move_made.emit(row, col)
        self.move_made.emit(self.block_value, row, col)
        


    def check_winner_in_block(self, current_player):
        for row in range(3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == current_player:
                return True

        for col in range(3):
            if self.board[0][col] == self.board[1][col] == self.board[2][col] == current_player:
                return True

        if self.board[0][0] == self.board[1][1] == self.board[2][2] == current_player:
            return True

        if self.board[0][2] == self.board[1][1] == self.board[2][0] == current_player:
            return True

        return False


    def check_draw_in_block(self):
            for row in range(3):
                for col in range(3):
                    if self.board[row][col] is None:
                        return False
            return True



    def show_single_button(self, current_player):
        for row in range(3):
            for col in range(3):
                button = self.buttons[row][col]
                if button is not None:
                    button.hide()

        winner_button = QPushButton(self)
        winner_button.setFixedSize(250, 250)
        winner_button.setFont(QFont("Times New Roman", 120))
        winner_button.setText(f"{current_player}")

        symbol_color = self.canva.x_color.name() if current_player == "X" else self.canva.o_color.name()
        winner_button.setStyleSheet(f"""QPushButton {{background-color: {self.canva.canva_color.name()};
                                                        color: {symbol_color}}}""")
        rowLayout = self.layout().itemAt(0)
        gameField = rowLayout.itemAt(0).widget()
        gameLayout = gameField.layout()
        gameLayout.addWidget(winner_button)
        gameLayout.setAlignment(winner_button, Qt.AlignmentFlag.AlignCenter)

        self.block_value = current_player



    def setBackground(self):
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    self.buttons[row][col].setStyleSheet("""QPushButton 
                    {background-color: rgba(255, 255, 0, 0.3); color: black;}""")
                else:
                    self.buttons[row][col].setStyleSheet("QPushButton {background-color: transparent; color: black;}")
                    self.buttons[row][col].setEnabled(False)


    def clean_Background(self):
        for row in range(3):
            for col in range(3):
                if self.buttons[row][col] != "":
                    self.buttons[row][col].setStyleSheet("background-color: transparent;")

