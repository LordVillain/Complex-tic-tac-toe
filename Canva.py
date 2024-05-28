from PyQt6.QtGui import QColor, QPainter, QPen, QBrush,QPixmap
from PyQt6.QtWidgets import  QLabel,QWidget, QColorDialog

class Canva(QWidget):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.label = QLabel()
        self.canvas = QPixmap(740, 740)
        self.canvas.fill(QColor("black"))
        self.label.setGeometry(0, 0, self.canvas.width(), self.canvas.height())

        self.x_color = QColor("white")
        self.o_color = QColor("white")
        self.canva_color = QColor("#68829e")

        self.draw_border(self.canva_color)
        self.draw_lines()
        self.draw_little_lines()
        self.label.setPixmap(self.canvas)
        self.occupied_cells = [[False for _ in range(9)] for _ in range(9)]

 

    def choose_color_x(self):
        color = QColorDialog.getColor(self.x_color, self)
        if color.isValid():
            self.x_color = color

    def choose_color_o(self):
        color = QColorDialog.getColor(self.o_color, self)
        if color.isValid():
            self.o_color = color

    def choose_color_canva(self):
        color = QColorDialog.getColor(self.canva_color, self)
        if color.isValid():
            self.canva_color = color
            self.parent().menuBar.save()
            self.parent().big_field.clear_field()
            self.parent().menuBar.load()



    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.canvas)

    def draw_border(self, canva_color):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setWidth(10)
        pen.setColor(QColor("black"))
        painter.setPen(pen)
        brush = QBrush(canva_color)
        painter.setBrush(brush)

        painter.drawRect(0, 0, 740, 740)

    def draw_lines(self):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setWidth(9)
        pen.setColor(QColor("black"))
        painter.setPen(pen)

        painter.drawLine(0, self.canvas.height() // 3, self.canvas.width(), self.canvas.height() // 3)
        painter.drawLine(0, (self.canvas.height() // 3) * 2, self.canvas.width(), (self.canvas.height() // 3) * 2)

        painter.drawLine(self.canvas.width() // 3, 0, self.canvas.width() // 3, self.canvas.height())
        painter.drawLine((self.canvas.width() // 3) * 2, 0, (self.canvas.width() // 3) * 2, self.canvas.height())

    def draw_little_lines(self):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setWidth(5)
        pen.setColor(QColor("black"))
        painter.setPen(pen)

        painter.drawLine(0, self.canvas.height() // 9, self.canvas.width(), self.canvas.height() // 9)
        painter.drawLine(0, (self.canvas.height() // 9) * 2, self.canvas.width(), (self.canvas.height() // 9) * 2)

        painter.drawLine(0, (self.canvas.height() // 9) * 4+4, self.canvas.width(), (self.canvas.height() // 9) * 4+4)
        painter.drawLine(0, (self.canvas.height() // 9)* 5, self.canvas.width(), (self.canvas.height() // 9)*5)

        painter.drawLine(0, (self.canvas.height() // 9) *7+4, self.canvas.width(), (self.canvas.height() // 9)*7+4)
        painter.drawLine(0, (self.canvas.height() // 9) * 8, self.canvas.width(), (self.canvas.height() // 9) * 8)

        painter.drawLine(self.canvas.width() // 9, 0, self.canvas.width() // 9, self.canvas.height())
        painter.drawLine((self.canvas.width() // 9) * 2, 0, (self.canvas.width() // 9) * 2, self.canvas.height())

        painter.drawLine((self.canvas.width() // 9)*4, 0,(self.canvas.width() // 9)*4, self.canvas.height())
        painter.drawLine((self.canvas.width() // 9) * 5, 0, (self.canvas.width() // 9) * 5, self.canvas.height())

        painter.drawLine((self.canvas.width() // 9)*7+4, 0, (self.canvas.width() // 9)*7+4, self.canvas.height())
        painter.drawLine((self.canvas.width() // 9) * 8, 0, (self.canvas.width() // 9) * 8, self.canvas.height())



    def draw_symbol(self, row_in_field, col_in_field, row_in_block, col_in_block, symbol):
        painter = QPainter(self.canvas)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen()
        pen.setWidth(10)
        pen.setColor(QColor("white"))
        painter.setPen(pen)

        brush = QBrush(self.canva_color)
        painter.setBrush(brush)

        cell_width = self.canvas.width() // 9
        cell_height = self.canvas.height() // 9
        block_width = cell_width * 3
        block_height = cell_height * 3
        center_x = int(col_in_field * block_width + (col_in_block + 0.5) * cell_width)
        center_y = int(row_in_field * block_height + (row_in_block + 0.5) * cell_height)

        block_index = row_in_field * 3 + col_in_field
        if not self.occupied_cells[block_index][row_in_block * 3 + col_in_block]:
            if symbol == "X":
                pen.setColor(self.x_color)
                painter.setPen(pen)
                painter.drawLine(center_x - cell_width // 4, center_y - cell_height // 4,
                                center_x + cell_width // 4, center_y + cell_height // 4)
                painter.drawLine(center_x - cell_width // 4, center_y + cell_height // 4,
                                center_x + cell_width // 4, center_y - cell_height // 4)
                self.occupied_cells[block_index][row_in_block * 3 + col_in_block] = True
            elif symbol == "O":
                pen.setColor(self.o_color)
                painter.setPen(pen)
                painter.drawEllipse(center_x - cell_width // 4, center_y - cell_height // 4,
                                    cell_width // 2, cell_height // 2)
                self.occupied_cells[block_index][row_in_block * 3 + col_in_block] = True

                

    def reset_canvas(self):
        self.canvas.fill(QColor("black"))
        self.draw_border(self.canva_color)
        self.draw_lines()
        self.draw_little_lines()
        self.occupied_cells = [[False for _ in range(9)] for _ in range(9)]
        self.label.setPixmap(self.canvas)