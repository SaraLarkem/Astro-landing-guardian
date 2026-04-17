from PyQt5.QtWidgets import QDialog, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class ResultDialog(QDialog):
    def __init__(self, status, accuracy, matrix, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Prediction Result")
        self.setFixedSize(420, 380)
        self.setStyleSheet("""
            background-color: #000000; 
            border: 2px solid #00AFFF;
            border-radius: 12px;
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)

        # Title
        title = QLabel("Landing Safety Result")
        title.setFont(QFont("Orbitron", 14, QFont.Bold))
        title.setStyleSheet("color: #00AFFF;")
        title.setAlignment(Qt.AlignCenter)

        # Status (SAFE / UNSAFE)
        status_label = QLabel(f" {status}")
        status_label.setFont(QFont("Orbitron", 18, QFont.Bold))
        status_label.setAlignment(Qt.AlignCenter)

        if status == "SAFE":
            status_label.setStyleSheet("color: #00FF7F;")  # green
        else:
            status_label.setStyleSheet("color: #FF4444;")  # red

        # Accuracy
        acc_label = QLabel(f"Model Accuracy: {accuracy:.2f}%")
        acc_label.setFont(QFont("Orbitron", 12))
        acc_label.setStyleSheet("color: #FFD972;")
        acc_label.setAlignment(Qt.AlignCenter)

        # Confusion matrix
        matrix_label = QLabel("Confusion Matrix:")
        matrix_label.setFont(QFont("Orbitron", 12))
        matrix_label.setStyleSheet("color: #00AFFF;")

        matrix_text = QLabel(str(matrix))
        matrix_text.setFont(QFont("Consolas", 11))
        matrix_text.setStyleSheet("color: white;")
        matrix_text.setAlignment(Qt.AlignCenter)

        # Close button
        close_btn = QPushButton("OK")
        close_btn.setFont(QFont("Orbitron", 12, QFont.Bold))
        close_btn.setStyleSheet("""
            QPushButton {
                color: #00AFFF;
                border: 2px solid #00AFFF;
                padding: 6px 12px;
                border-radius: 10px;
                background-color: transparent;
            }
            QPushButton:hover {
                background-color: rgba(0, 170, 255, 50);
            }
            QPushButton:pressed {
                background-color: #00AFFF;
                color: black;
            }
        """)
        close_btn.clicked.connect(self.close)

        # Add widgets to layout
        layout.addWidget(title)
        layout.addWidget(status_label)
        layout.addSpacing(10)
        layout.addWidget(acc_label)
        layout.addSpacing(10)
        layout.addWidget(matrix_label)
        layout.addWidget(matrix_text)
        layout.addSpacing(20)
        layout.addWidget(close_btn, alignment=Qt.AlignCenter)

        self.setLayout(layout)
