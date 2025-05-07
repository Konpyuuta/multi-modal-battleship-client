class SimpleHeartRateDisplay(QWidget):
    """Simple widget for displaying heart rate"""

    def __init__(self, player_name, parent=None):
        super().__init__(parent)
        self.player_name = player_name
        self.current_hr = 0
        self.update_threshold = 3.0  # Only update if change is greater than 3 BPM

        layout = QVBoxLayout()

        # Simple label for heart rate
        self.hr_label = QLabel(f"{player_name}'s Heart Rate: -- BPM")
        self.hr_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(self.hr_label)

        self.setLayout(layout)

    def update_heart_rate(self, heart_rate):
        """Update the display with a new heart rate value"""
        # Only update if the change is significant
        if abs(self.current_hr - heart_rate) < self.update_threshold:
            return

        self.current_hr = heart_rate
        self.hr_label.setText(f"{self.player_name}'s Heart Rate: {heart_rate:.1f} BPM")