import sys
import os
import random
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QTimer, Qt

class DiceApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("주사위 던지기")
        self.setGeometry(100, 100, 400, 500)

        self.dice_images = []
        self.load_dice_images()

        self.init_ui()
        self.rolling = False
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_dice_image)

    def load_dice_images(self):
        base_path = "C:/Users/park0/github/gemini-cli-tutorial/Dice/images/"
        for i in range(1, 7):
            image_path = os.path.join(base_path, f"dice{i}.png")
            if os.path.exists(image_path):
                self.dice_images.append(QPixmap(image_path))
            else:
                print(f"Warning: Image not found at {image_path}")
        if not self.dice_images:
            print("Error: No dice images loaded. Please check the path and file names.")

    def init_ui(self):
        layout = QVBoxLayout()

        self.dice_label = QLabel(self)
        self.dice_label.setAlignment(Qt.AlignCenter)
        if self.dice_images:
            self.dice_label.setPixmap(random.choice(self.dice_images).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.dice_label.setText("No dice image available")
        layout.addWidget(self.dice_label)

        self.roll_button = QPushButton("주사위 던지기", self)
        self.roll_button.clicked.connect(self.toggle_roll)
        layout.addWidget(self.roll_button)

        self.setLayout(layout)

    def toggle_roll(self):
        if not self.dice_images:
            print("Cannot roll dice: No images loaded.")
            return

        if not self.rolling:
            # Start rolling
            self.rolling = True
            self.roll_button.setText("선택 버튼")
            self.timer.start(100)  # Update every 100 ms (10 times per second)
        else:
            # Stop rolling
            self.rolling = False
            self.roll_button.setText("주사위 던지기")
            self.timer.stop()

    def update_dice_image(self):
        if self.dice_images:
            self.dice_label.setPixmap(random.choice(self.dice_images).scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = DiceApp()
    ex.show()
    sys.exit(app.exec_())
