from PyQt6.QtWidgets import QMenuBar, QMenu, QWidget, QColorDialog, QFileDialog
from PyQt6.QtGui import QAction, QColor, QPixmap
import json

class TestMenu(QMenuBar):
    def __init__(self, parent: QWidget):
        super().__init__(parent)
        self.setMinimumSize(300, 1)
        
        self.stateMItem = QMenu("State")
        self.fileMItem = QMenu("File")
        self.decorMItem = QMenu("Edit")
        
        self.addMenu(self.stateMItem)
        self.addMenu(self.decorMItem)
        self.addMenu(self.fileMItem)

        self.saveMenuAction = QAction("Save the game")
        self.stateMItem.addAction(self.saveMenuAction)

        self.loadMenuAction = QAction("Continue the game")
        self.stateMItem.addAction(self.loadMenuAction)

        self.Start_again = QAction("Start again")
        self.fileMItem.addAction(self.Start_again)
        self.Start_again.triggered.connect(self.parent().big_field.clear_field)

        self.color_canva_action = QAction("Цвет поля")
        self.color_x_action = QAction("Цвет X")
        self.color_o_action = QAction("Цвет O")

        self.decorMItem.addAction(self.color_canva_action)
        self.decorMItem.addAction(self.color_x_action)
        self.decorMItem.addAction(self.color_o_action)

        self.color_x_action.triggered.connect(self.parent().canvas.choose_color_x)
        self.color_o_action.triggered.connect(self.parent().canvas.choose_color_o)
        self.color_canva_action.triggered.connect(self.parent().canvas.choose_color_canva)



    def save(self):

        try:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Game", "", "JSON Files (*.json)")
            if file_path:
                self.mini_blocks = self.parent().big_field.small_blocks
                game_state = {

                    "player1_name": self.parent().player1.get_name(),
                    "player2_name": self.parent().player2.get_name(),
                    "current_player": self.parent().big_field.Get_current_player(),
                    "locked_row": self.parent().big_field.blocked_row, 
                    "locked_col": self.parent().big_field.blocked_col,
                    "x_color": self.parent().canvas.x_color.name(),
                    "o_color": self.parent().canvas.o_color.name(),
                    "canva_color": self.parent().canvas.canva_color.name(),   
                            
                    "small_blocks": [
            [
                {
                    "block_value": self.parent().big_field.small_blocks[i][j].block_value,
                    "buttons": [
                        [self.parent().big_field.small_blocks[i][j].board[x][y] for y in range(3)]
                        for x in range(3)
                    ],
                }
                for j in range(3)
            ]
            for i in range(3)
            ]      
                            }
            with open(file_path, "w") as file:
                json.dump(game_state, file, indent=2)
        except Exception as e:
            print(f"Error saving game state: {e}")

    
    def load(self):

        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Load Game", "", "JSON Files (*.json)")
            if file_path:
                self.parent().big_field.clear_field()
                with open(file_path, "r") as file:
                    game_state = json.load(file)

                self.parent().big_field.set_player_names(game_state["player1_name"], game_state["player2_name"])
                self.parent().player1.button_player_name.setText(game_state["player1_name"])
                self.parent().player2.button_player_name.setText(game_state["player2_name"])

                self.parent().big_field.Set_current_player(game_state["current_player"])

                self.parent().canvas.x_color = QColor(game_state["x_color"])
                self.parent().canvas.o_color = QColor(game_state["o_color"])
                self.parent().canvas.canva_color = QColor(game_state["canva_color"])

                for j in range(3):
                    for i in range(3):
                        self.parent().big_field.small_blocks[i][j].block_value = game_state["small_blocks"][i][j]["block_value"]
                        if game_state["small_blocks"][i][j]["block_value"] != "":
                            self.parent().big_field.small_blocks[i][j].show_single_button(game_state["small_blocks"][i][j]["block_value"])

                        for y in range(3):
                            for x in range(3):
                                if game_state["small_blocks"][i][j]["buttons"][x][y] == "X":
                                    self.parent().canvas.draw_symbol(i, j, x, y, "X")
                                    self.parent().big_field.small_blocks[i][j].board[x][y] = "X"

                                elif game_state["small_blocks"][i][j]["buttons"][x][y] == "O":
                                    self.parent().canvas.draw_symbol(i, j, x, y, "O")
                                    self.parent().big_field.small_blocks[i][j].board[x][y] = "O"
                                    
                self.parent().big_field.right_move(game_state["locked_row"], game_state["locked_col"])

        except Exception as e:
            print(f"Error loading game state: {e}")