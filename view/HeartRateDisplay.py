# HeartRateDisplay.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor


class HeartRateDisplay(QWidget):
    """Widget for displaying a player's heart rate"""

    def __init__(self, player_name, parent=None):
        super().__init__(parent)
        self.player_name = player_name
        self.current_hr = 0
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Title label
        self.title_label = QLabel(f"{self.player_name}'s Heart Rate")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px;")

        # Heart rate value
        self.hr_label = QLabel("-- BPM")
        self.hr_label.setAlignment(Qt.AlignCenter)
        self.hr_label.setStyleSheet("font-size: 24px; color: #2196F3;")

        # Heart rate bar
        self.hr_bar = QProgressBar()
        self.hr_bar.setRange(50, 150)  # Typical heart rate range
        self.hr_bar.setValue(75)  # Default value
        self.hr_bar.setTextVisible(False)
        self.hr_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 4px;
                background-color: #f0f0f0;
            }
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #88ff88, stop:0.5 #ffff00, stop:1 #ff8888);
            }
        """)

        # Status label
        self.status_label = QLabel("Normal")
        self.status_label.setAlignment(Qt.AlignCenter)

        # Add widgets to layout
        layout.addWidget(self.title_label)
        layout.addWidget(self.hr_label)
        layout.addWidget(self.hr_bar)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def update_heart_rate(self, heart_rate):
        """Update the display with a new heart rate value"""
        self.current_hr = heart_rate
        self.hr_label.setText(f"{heart_rate:.1f} BPM")
        self.hr_bar.setValue(min(max(int(heart_rate), 50), 150))

        # Update status text and color based on heart rate
        if heart_rate > 100:
            self.status_label.setText("Elevated")
            self.status_label.setStyleSheet("color: red;")
        elif heart_rate > 80:
            self.status_label.setText("Active")
            self.status_label.setStyleSheet("color: orange;")
        else:
            self.status_label.setText("Normal")
            self.status_label.setStyleSheet("color: green;")