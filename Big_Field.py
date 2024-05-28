from PyQt6.QtWidgets import QWidget, QGridLayout, QMessageBox, QVBoxLayout, QHBoxLayout
from Small_Field import Small_Field

class Big_Field(QWidget):
    def __init__(self, parent: QWidget, canva):
        super().__init__(parent)

        self.canva = canva

        Big_mainLayout = QVBoxLayout(self)
        Big_mainLayout.setSpacing(0)

        Big_rowLayout = QHBoxLayout()
        Big_rowLayout.setSpacing(0)

        Big_game_Field = QWidget()
        Big_game_Field.setFixedSize(750, 750)
        self.layout = QGridLayout(Big_game_Field)

        self.player1_name = "player_X"
        self.player2_name = "player_O"

        self.small_blocks = [[Small_Field(self, canva) for _ in range(3)] for _ in range(3)]
        self.blocked_row = 0
        self.blocked_col = 0

        for row in range(3):
            for col in range(3):
                field = self.small_blocks[row][col]
                field.setFixedSize(255, 255)
                field.setContentsMargins(0, 0, 0, 0)
                field.move_made.connect(self.click_move_made)
                field.right_move_made.connect(self.right_move)
                self.layout.addWidget(field, row, col)

        Big_rowLayout.addWidget(Big_game_Field)
        Big_mainLayout.addLayout(Big_rowLayout)



    def set_player_names(self, player1_name, player2_name):
        self.player1_name = player1_name or "Player_X"
        self.player2_name = player2_name or "Player_O"



    def click_move_made(self, block_value, row, col):

        button = self.sender()

        for i, row_layout in enumerate(self.small_blocks):
            for j, field in enumerate(row_layout):
                if field is button:
                    row_in_field = i 
                    col_in_field = j
                    break
            else:
                continue
            break
        self.symbol = self.Get_current_player()

        self.canva.draw_symbol(row_in_field, col_in_field, row, col, self.symbol)

        winner_name = self.player1_name if self.Get_current_player() == "X" else self.player2_name

        if self.check_winner(block_value):
            self.anblocking()
            msg = QMessageBox()
            msg.setWindowTitle("Игра завершена")
            msg.setText(f"Игрок {winner_name} победил!")
            msg.setStyleSheet("QMessageBox {background-color: #D3D3D3; font-size: 30px;}")
            msg.exec()
            self.clear_field()
            
        elif self.check_draw():
            self.anblocking()
            msg = QMessageBox()
            msg.setWindowTitle("Игра завершена")
            msg.setText("     Ничья!     ")
            msg.setStyleSheet("QMessageBox {background-color: #D3D3D3; font-size: 30px;}")
            msg.exec()
            self.clear_field()

        else:
            self.Set_current_player("O") if self.Get_current_player() == "X" else self.Set_current_player("X")
    


    def right_move(self, row, col):
        self.blocked_row = row
        self.blocked_col = col
        self.anblocking()
        if self.small_blocks[row][col].block_value == "":
            self.blocking(row, col)
        else:
            for big_row in range(3):
                for big_col in range(3):
                    self.small_blocks[big_row][big_col].setBackground()

    def blocking(self, row, col):
        for big_row in range(3):
            for big_col in range(3):
                if big_row != row or big_col != col:
                    self.small_blocks[big_row][big_col].setEnabled(False)
                else:
                    self.small_blocks[row][col].setBackground()

    def anblocking(self):
        for big_row in range(3):
            for big_col in range(3):
                self.small_blocks[big_row][big_col].setEnabled(True)
                self.small_blocks[big_row][big_col].clean_Background()
                


    def Set_current_player(self, new_value):
        for row in range(3):
            for col in range(3):
                self.small_blocks[row][col].current_player = new_value


    def Get_current_player(self):
        for row in range(3):
            for col in range(3):
                return self.small_blocks[row][col].current_player



    def check_winner(self, block_value):
        for row in range(3):
            if self.small_blocks[row][0].block_value == self.small_blocks[row][1].block_value == self.small_blocks[row][2].block_value == block_value and self.small_blocks[row][0].block_value != "":
                return True

        for col in range(3):
            if self.small_blocks[0][col].block_value == self.small_blocks[1][col].block_value == self.small_blocks[2][col].block_value == block_value and self.small_blocks[0][col].block_value != "":
                return True

        if self.small_blocks[0][0].block_value == self.small_blocks[1][1].block_value == self.small_blocks[2][2].block_value == block_value and self.small_blocks[0][0].block_value != "":
            return True

        if self.small_blocks[0][2].block_value == self.small_blocks[1][1].block_value == self.small_blocks[2][0].block_value == block_value and self.small_blocks[0][2].block_value != "":
            return True
        return False

    def check_draw(self):
        for row in range(3):
            for col in range(3):
                if self.small_blocks[row][col].block_value == "":
                    return False
        return True
    

        
    def clear_field(self):
        self.canva.reset_canvas()
        self.anblocking()
        for row in range(3):
            for col in range(3):
                field = self.small_blocks[row][col]
                self.layout.removeWidget(field)
                field.deleteLater()
                self.small_blocks[row][col] = None
        self.small_blocks = [[Small_Field(self, self.canva) for _ in range(3)] for _ in range(3)]

        for row in range(3):
            for col in range(3):
                field = self.small_blocks[row][col]
                field.setFixedSize(255, 255)
                field.setContentsMargins(0, 0, 0, 0)
                field.move_made.connect(self.click_move_made)
                field.right_move_made.connect(self.right_move)
                self.layout.addWidget(field, row, col)
        