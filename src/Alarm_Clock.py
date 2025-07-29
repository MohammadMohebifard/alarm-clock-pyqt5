import sys
import os
import threading
import pygame
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTimeEdit, QPushButton, QMessageBox, QGroupBox, QFileDialog
)
from PyQt5.QtCore import QTime, QTimer


class AlarmClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Alarm Clock")
        self.resize(400, 260)

        self.setStyleSheet("""
    QWidget {
        background-color: #2c3e50;
        color: #ecf0f1;
        font-family: Segoe UI;
        font-size: 14px;
    }
    QPushButton {
        background-color: #27ae60;
        color: white;
        border-radius: 6px;
        padding: 6px 12px;
    }
    QPushButton:hover {
        background-color: #1e8449;
    }
    QGroupBox {
        border: 1px solid #34495e;
        margin-top: 10px;
        padding: 10px;
        border-radius: 6px;
    }
    QGroupBox::title {
        subcontrol-origin: margin;
        left: 10px;
        padding: 0 3px 0 3px;
    }
    QLabel {
        color: #ecf0f1;
    }
    QTimeEdit {
        background-color: #34495e;
        color: #ecf0f1;
        border-radius: 4px;
        padding: 4px;
    }
""")

        layout = QVBoxLayout()

        self.current_time_label = QLabel()
        self.update_current_time()
        layout.addWidget(self.current_time_label)

        alarm_group = QGroupBox("Alarm Settings")
        group_layout = QVBoxLayout()

        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        group_layout.addWidget(self.time_edit)

        self.remaining_label = QLabel("Time remaining: N/A")
        group_layout.addWidget(self.remaining_label)

        file_button_layout = QHBoxLayout()
        self.select_sound_button = QPushButton("Choose Alarm Sound")
        self.select_sound_button.clicked.connect(self.choose_sound)
        file_button_layout.addWidget(self.select_sound_button)

        self.sound_file_label = QLabel("No file selected")
        file_button_layout.addWidget(self.sound_file_label)

        group_layout.addLayout(file_button_layout)

        button_layout = QHBoxLayout()
        self.set_button = QPushButton("Set Alarm")
        self.set_button.clicked.connect(self.set_alarm)
        button_layout.addWidget(self.set_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_alarm)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button)

        group_layout.addLayout(button_layout)
        alarm_group.setLayout(group_layout)
        layout.addWidget(alarm_group)

        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_alarm)
        self.timer.timeout.connect(self.update_current_time)
        self.timer.start(1000)

        self.alarm_time = None
        self.alarm_active = False
        self.sound_file = None

    def update_current_time(self):
        self.current_time_label.setText("Current time: " + QTime.currentTime().toString("HH:mm:ss"))

    def choose_sound(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Choose Sound File", "", "Audio Files (*.mp3 *.wav)")
        if file_path:
            self.sound_file = file_path
            self.sound_file_label.setText(os.path.basename(file_path))

    def set_alarm(self):
        if not self.sound_file:
            QMessageBox.warning(self, "No Sound Selected", "Please choose a sound file for the alarm.")
            return

        self.alarm_time = self.time_edit.time()
        self.alarm_active = True
        self.cancel_button.setEnabled(True)
        QMessageBox.information(self, "Alarm Set", f"Alarm set for {self.alarm_time.toString('HH:mm')}")

    def cancel_alarm(self):
        self.alarm_time = None
        self.alarm_active = False
        self.cancel_button.setEnabled(False)
        self.remaining_label.setText("Time remaining: N/A")
        QMessageBox.information(self, "Alarm Canceled", "Alarm has been canceled.")

    def play_alarm_sound(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
        except Exception as e:
            QMessageBox.warning(self, "Sound Error", f"Could not play sound:\n{e}")

    def check_alarm(self):
        if self.alarm_time and self.alarm_active:
            current_time = QTime.currentTime()
            seconds_left = current_time.secsTo(self.alarm_time)
            if seconds_left <= 0:
                self.alarm_active = False
                self.cancel_button.setEnabled(False)
                self.remaining_label.setText("Time remaining: N/A")
                threading.Thread(target=self.play_alarm_sound, daemon=True).start()
            else:
                mins, secs = divmod(seconds_left, 60)
                self.remaining_label.setText(f"Time remaining: {mins:02}:{secs:02}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    clock = AlarmClock()
    clock.show()
    sys.exit(app.exec_())
