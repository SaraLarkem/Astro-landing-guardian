import sys
import os
import winsound
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QPushButton
from sklearn.metrics import confusion_matrix
from landing_ui import Ui_MainWindow
from MySpaceDecisionTree import MySpaceDecisionTree


class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.music_file = "ytmp3free.cc_steinsgate-ost-explanation-youtubemp3free.org.wav"
        self.music_muted = False
        self.music_available = False

        # Load + train ML model
        self.model = MySpaceDecisionTree()
        self.acc, self.matrix = self.model.train()

        # Tracks confusion matrix from user-entered cases with known actual outcome.
        self.live_true = []
        self.live_pred = []

        # Connect buttons
        self.ui.btn_predict.clicked.connect(self.run_prediction)

        if hasattr(self.ui, "btn_reset"):
            self.ui.btn_reset.clicked.connect(self.reset_fields)
            self.style_reset_button()

        self.add_mute_button()

        # Start looping background music if file exists.
        self.start_background_music()

    # ---------------------------------------------------------------
    def safe_get(self, widget):
        if widget is None:
            raise RuntimeError("A widget is missing! Check objectName in Qt Designer.")
        return widget

    # ---------------------------------------------------------------
    def style_reset_button(self):
        """Apply consistent neon button style to Reset."""
        # Keep Reset perfectly aligned under Predict.
        self.ui.btn_reset.setGeometry(250, 500, 121, 28)
        self.ui.btn_reset.setStyleSheet(
            "QPushButton {"
            "    background-color: transparent;"
            "    color: #00AFFF;"
            "    border: 2px solid #00AFFF;"
            "    border-radius: 10px;"
            "    padding: 6px 12px;"
            "    font-family: Orbitron;"
            "    font-size: 16px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgba(0, 170, 255, 40);"
            "}"
            "QPushButton:pressed {"
            "    color: black;"
            "    background-color: #00AFFF;"
            "}"
        )

    # ---------------------------------------------------------------
    def style_message_box(self, box):
        """Give popups the same app visual style."""
        box.setStyleSheet(
            "QMessageBox {"
            "    background-color: #0E1B2E;"
            "    color: #F4FBFF;"
            "    border: 2px solid #00AFFF;"
            "}"
            "QLabel {"
            "    color: #F4FBFF;"
            "    font-family: Orbitron;"
            "    font-size: 14px;"
            "}"
            "QPushButton {"
            "    min-width: 90px;"
            "    background-color: transparent;"
            "    color: #00AFFF;"
            "    border: 2px solid #00AFFF;"
            "    border-radius: 8px;"
            "    padding: 6px 10px;"
            "    font-family: Orbitron;"
            "    font-size: 11px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgba(0, 170, 255, 40);"
            "}"
            "QPushButton:pressed {"
            "    color: black;"
            "    background-color: #00AFFF;"
            "}"
        )

    # ---------------------------------------------------------------
    def start_background_music(self):
        """Loop local WAV file asynchronously in the background."""
        music_path = os.path.join(os.path.dirname(__file__), self.music_file)
        if not os.path.exists(music_path):
            self.music_available = False
            print(f"[MUSIC] File not found: {music_path}")
            return
        try:
            winsound.PlaySound(
                music_path,
                winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP,
            )
            self.music_available = True
            self.music_muted = False
            print(f"[MUSIC] Playing in background: {self.music_file}")
        except Exception as e:
            self.music_available = False
            print(f"[MUSIC ERROR] {e}")

    # ---------------------------------------------------------------
    def stop_background_music(self):
        """Stop any currently playing winsound audio."""
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
            self.music_muted = True
            print("[MUSIC] Stopped")
        except Exception as e:
            print(f"[MUSIC STOP ERROR] {e}")

    # ---------------------------------------------------------------
    def add_mute_button(self):
        """Create an in-code mute/unmute toggle button."""
        self.btn_mute = QPushButton("Mute", self.ui.centralwidget)
        self.btn_mute.setGeometry(480, 500, 93, 28)
        self.btn_mute.setStyleSheet(
            "QPushButton {"
            "    background-color: transparent;"
            "    color: #00AFFF;"
            "    border: 2px solid #00AFFF;"
            "    border-radius: 10px;"
            "    padding: 4px 8px;"
            "    font-family: Orbitron;"
            "    font-size: 12px;"
            "    font-weight: bold;"
            "}"
            "QPushButton:hover {"
            "    background-color: rgba(0, 170, 255, 40);"
            "}"
            "QPushButton:pressed {"
            "    color: black;"
            "    background-color: #00AFFF;"
            "}"
        )
        self.btn_mute.clicked.connect(self.toggle_mute)

    # ---------------------------------------------------------------
    def toggle_mute(self):
        """Toggle background music state."""
        if not self.music_available:
            msg = QMessageBox(self)
            msg.setWindowTitle("Music unavailable")
            msg.setText("Background music file was not found.")
            self.style_message_box(msg)
            msg.exec_()
            return

        if self.music_muted:
            self.start_background_music()
            self.btn_mute.setText("Mute")
        else:
            self.stop_background_music()
            self.btn_mute.setText("Unmute")

    # ---------------------------------------------------------------
    def closeEvent(self, event):
        self.stop_background_music()
        super().closeEvent(event)

    # ---------------------------------------------------------------
    def run_prediction(self):
        """Collect values from UI, run ML prediction, show popup"""
        try:
            # Numeric values
            atmosphere  = self.safe_get(self.ui.input_atmosphere).value()
            gravity     = self.safe_get(self.ui.input_gravity).value()
            temperature = self.safe_get(self.ui.input_temperature).value()
            radiation   = self.safe_get(self.ui.input_radiation).value()
            wind        = self.safe_get(self.ui.input_wind).value()
            toxicity    = self.safe_get(self.ui.input_toxicity).value()

            # Combo boxes
            water_text = self.safe_get(self.ui.combo_water).currentText()
            terrain    = self.safe_get(self.ui.combo_terrain).currentText()

            water = 1 if "Present" in water_text else 0

            # Debugging (helps check UI)
            print(
                f"[DEBUG INPUTS] Atmos={atmosphere}, Grav={gravity}, Temp={temperature}, "
                f"Rad={radiation}, Water={water}, Wind={wind}, Toxic={toxicity}, Terrain={terrain}"
            )

            # --------------------------------------------------------
            # IMPORTANT: CORRECT ORDER FOR PREDICT_SINGLE
            # --------------------------------------------------------
            result = self.model.predict_single(
                atmosphere,   # 1
                gravity,      # 2  ✔ FIXED
                temperature,  # 3  ✔ FIXED
                radiation,    # 4
                water,        # 5
                wind,         # 6
                toxicity,     # 7
                terrain       # 8
            )
            # --------------------------------------------------------

            self.capture_actual_outcome(result)
            self.show_result_popup(result)

        except Exception as e:
            msg = QMessageBox(self)
            msg.setWindowTitle("Error")
            msg.setText(f"<b>ERROR:</b><br>{e}")
            self.style_message_box(msg)
            msg.exec_()

    # ---------------------------------------------------------------
    def capture_actual_outcome(self, predicted_result):
        """
        Ask user for ground truth and update live confusion matrix.
        Yes  -> actual safe (1)
        No   -> actual unsafe (0)
        Cancel -> skip this sample
        """
        prompt = QMessageBox(self)
        prompt.setWindowTitle("Confirm Actual Outcome")
        prompt.setText(
            "Was this landing actually SAFE?\n\n"
            "Yes = Safe, No = Unsafe, Cancel = Skip"
        )
        prompt.setStandardButtons(
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel
        )
        self.style_message_box(prompt)
        choice = prompt.exec_()

        if choice == QMessageBox.Cancel:
            return

        actual = 1 if choice == QMessageBox.Yes else 0
        self.live_true.append(actual)
        self.live_pred.append(int(predicted_result))

    # ---------------------------------------------------------------
    def format_confusion_matrix(self):
        """
        Return a readable confusion matrix string:
        [[TN, FP],
         [FN, TP]]
        """
        try:
            tn, fp = self.matrix[0]
            fn, tp = self.matrix[1]
            return (
                "            Pred Unsafe  Pred Safe\n"
                f"Actual Unsafe    {tn:>5}      {fp:>5}\n"
                f"Actual Safe      {fn:>5}      {tp:>5}"
            )
        except Exception:
            # Fallback if matrix shape/type is unexpected
            return str(self.matrix)

    # ---------------------------------------------------------------
    def format_live_confusion_matrix(self):
        """Return confusion matrix computed from user-confirmed inputs."""
        if not self.live_true:
            return "No confirmed samples yet."

        cm = confusion_matrix(self.live_true, self.live_pred, labels=[0, 1])
        tn, fp = cm[0]
        fn, tp = cm[1]
        return (
            "            Pred Unsafe  Pred Safe\n"
            f"Actual Unsafe    {tn:>5}      {fp:>5}\n"
            f"Actual Safe      {fn:>5}      {tp:>5}\n"
            f"\nSamples: {len(self.live_true)}"
        )

    # ---------------------------------------------------------------
    def show_result_popup(self, result):
        msg = QMessageBox(self)
        msg.setWindowTitle("Prediction Result")

        status = "SAFE TO LAND" if result == 1 else "UNSAFE TO LAND"
        colour = "#00FF00" if result == 1 else "#FF4444"
        live_matrix_text = self.format_live_confusion_matrix().replace("\n", "<br>")
        training_matrix_text = self.format_confusion_matrix().replace("\n", "<br>")

        msg.setText(
            f"<h2 style='color:{colour}; margin-bottom: 6px;'>{status}</h2>"
            f"<div style='font-size:14px; line-height:1.5;'>"
            f"<b>Model Accuracy (test split):</b> {self.acc * 100:.2f}%"
            f"<br><br><b>Live Confusion Matrix (your confirmed inputs)</b>"
            f"<br><span style='font-family:Consolas, monospace; color:#FFFFFF;'>{live_matrix_text}</span>"
            f"<br><br><b>Training Confusion Matrix (fixed reference)</b>"
            f"<br><span style='font-family:Consolas, monospace; color:#DDEFFF;'>{training_matrix_text}</span>"
            "<br><br><b>Legend</b>"
            "<br><span style='color:#2E7D32;'>TN/TP = correct predictions</span>"
            "<br><span style='color:#EF6C00;'>FP/FN = prediction mistakes</span>"
            "</div>"
        )

        self.style_message_box(msg)
        msg.exec_()

    # ---------------------------------------------------------------
    def reset_fields(self):
        """Reset UI fields"""
        try:
            self.ui.input_atmosphere.setValue(0)
            self.ui.input_gravity.setValue(0)
            self.ui.input_temperature.setValue(0)
            self.ui.input_radiation.setValue(0)
            self.ui.input_wind.setValue(0)
            self.ui.input_toxicity.setValue(0)

            self.ui.combo_water.setCurrentIndex(0)
            self.ui.combo_terrain.setCurrentIndex(0)
        except Exception as e:
            print(f"[ERROR during reset] {e}")


# ---------------------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
