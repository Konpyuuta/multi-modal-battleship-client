import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QLabel, QMainWindow, QVBoxLayout
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush, QPainterPath, QFont
from PyQt5.QtCore import Qt, QRect, QRectF, QPointF, QSize

from commands.requests.MoveRequest import MoveRequest
from commands.requests.RequestTypes import RequestTypes
from model.socket.SocketConnection import SocketConnection


class BattleshipCell(QWidget):
    """
    A widget representing a single cell in the battleship grid

    States:
    0 = no ship, no bomb (blue with waves)
    -1 = no ship, a bomb landed (blue with wave but more transparent, with a black cross)
    1 = a ship is there (ships connect visually with adjacent ship cells)
    2 = a ship is there and a bomb landed on it (like 1 but more transparent with a red cross)
    """

    _row = None

    _column = None

    def __init__(self, row, column, state=0, ship_connections=None, parent=None):
        super().__init__(parent)
        self.state = state
        # ship_connections is a dictionary with keys: 'top', 'right', 'bottom', 'left'
        # each value is True if there's a ship in that direction, False otherwise
        self.ship_connections = ship_connections or {'top': False, 'right': False, 'bottom': False, 'left': False}
        self.setMinimumSize(50, 50)
        self._row = row
        self._column = column

    def mousePressEvent(self, event):
        print(f'mousePressEvent: Row: {self._row} Column: {self._column}')
        move_request = MoveRequest(RequestTypes.MOVE_REQUEST, "Kuroro", self._row, self._column)
        s = SocketConnection("127.0.0.1", 8080)
        s.connect()
        s.send_request(move_request)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        rect = event.rect()

        # Define colors
        water_color = QColor(65, 105, 225)  # Royal blue
        transparent_water = QColor(65, 105, 225, 150)  # More transparent water
        ship_color = QColor(80, 80, 80)  # Dark gray
        hit_ship_color = QColor(80, 80, 80, 150)  # Transparent dark gray

        # Draw based on state
        if self.state == 0:  # Water (no ship, no bomb)
            self._draw_water(painter, rect, water_color)

        elif self.state == -1:  # Water hit (no ship, bomb landed)
            self._draw_water(painter, rect, transparent_water)
            self._draw_black_cross(painter, rect)

        elif self.state == 1:  # Ship (no hit)
            self._draw_ship(painter, rect, ship_color)

        elif self.state == 2:  # Ship hit
            self._draw_ship(painter, rect, hit_ship_color)
            self._draw_red_cross(painter, rect)

    def _draw_water(self, painter, rect, color):
        # Fill the background with water color
        painter.fillRect(rect, color)

        # Draw waves
        wave_pen = QPen(QColor(255, 255, 255, 100), 2, Qt.SolidLine)
        painter.setPen(wave_pen)

        # Draw 3 wavy lines
        height = rect.height()
        width = rect.width()

        for i in range(3):
            y_pos = height * (0.3 + i * 0.2)
            path = QPainterPath()
            path.moveTo(0, y_pos)

            # Create a wavy pattern
            segments = 4
            for j in range(segments + 1):
                control1_x = width * (j / segments) - width / (segments * 3)
                control1_y = y_pos - 5 if j % 2 == 0 else y_pos + 5
                control2_x = width * (j / segments) + width / (segments * 3)
                control2_y = y_pos - 5 if j % 2 == 0 else y_pos + 5
                end_x = width * (j / segments)
                end_y = y_pos

                path.cubicTo(
                    control1_x, control1_y,
                    control2_x, control2_y,
                    end_x, end_y
                )

            painter.drawPath(path)

    def _draw_black_cross(self, painter, rect):
        cross_pen = QPen(Qt.black, 3, Qt.SolidLine)
        painter.setPen(cross_pen)
        margin = int(rect.width() * 0.2)

        # Draw X using QPointF to handle float coordinates properly
        painter.drawLine(
            QPointF(margin, margin),
            QPointF(rect.width() - margin, rect.height() - margin)
        )
        painter.drawLine(
            QPointF(rect.width() - margin, margin),
            QPointF(margin, rect.height() - margin)
        )

    def _draw_red_cross(self, painter, rect):
        cross_pen = QPen(Qt.red, 3, Qt.SolidLine)
        painter.setPen(cross_pen)
        margin = int(rect.width() * 0.2)

        # Draw X using QPointF to handle float coordinates properly
        painter.drawLine(
            QPointF(margin, margin),
            QPointF(rect.width() - margin, rect.height() - margin)
        )
        painter.drawLine(
            QPointF(rect.width() - margin, margin),
            QPointF(margin, rect.height() - margin)
        )

    def _draw_ship(self, painter, rect, color):
        # Ship base color
        painter.fillRect(rect, color)

        # Draw ship with connections
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)

        # Margins for ship appearance
        margin = 5
        inner_rect = rect.adjusted(margin, margin, -margin, -margin)
        inner_rectf = QRectF(inner_rect)

        # Draw the base shape of the ship
        painter.fillRect(inner_rect, color)
        painter.drawRect(inner_rect)

        # Draw ship part indicators (< = >)
        text_pen = QPen(Qt.white, 2, Qt.SolidLine)
        painter.setPen(text_pen)
        painter.setFont(QFont("Arial", inner_rect.width() // 4))

        # Determine the ship part type based on connections
        is_horizontal = self.ship_connections['left'] or self.ship_connections['right']
        is_vertical = self.ship_connections['top'] or self.ship_connections['bottom']

        # If both horizontal and vertical connections exist, it's a special case (like a cross)
        # In that case, we'll just draw a plus sign
        if is_horizontal and is_vertical:
            painter.drawText(inner_rect, Qt.AlignCenter, "+")
        elif is_horizontal:
            # Horizontal ship part
            if self.ship_connections['left'] and self.ship_connections['right']:
                # Middle section
                painter.drawText(inner_rect, Qt.AlignCenter, "=")
            elif self.ship_connections['left']:
                # Right end
                painter.drawText(inner_rect, Qt.AlignCenter, ">")
            elif self.ship_connections['right']:
                # Left end
                painter.drawText(inner_rect, Qt.AlignCenter, "<")
            else:
                # Single piece (both ends)
                painter.drawText(inner_rect, Qt.AlignCenter, "<>")
        elif is_vertical:
            # Vertical ship part
            if self.ship_connections['top'] and self.ship_connections['bottom']:
                # Middle section (using = rotated)
                painter.drawText(inner_rect, Qt.AlignCenter, "‖")
            elif self.ship_connections['top']:
                # Bottom end (using v)
                painter.drawText(inner_rect, Qt.AlignCenter, "v")
            elif self.ship_connections['bottom']:
                # Top end (using ^)
                painter.drawText(inner_rect, Qt.AlignCenter, "^")
            else:
                # Single piece (both ends)
                painter.drawText(inner_rect, Qt.AlignCenter, "^v")
        else:
            # Isolated piece (a small ship)
            painter.drawText(inner_rect, Qt.AlignCenter, "<>");
