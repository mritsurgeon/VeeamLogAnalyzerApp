import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QTextEdit, QCheckBox, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from datetime import datetime
import re
import webbrowser

class LogAnalyzerApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Veeam Log Analyzer")
        self.setGeometry(100, 100, 1200, 800)

        self.logs = []
        self.filtered_logs = []

        self.initUI()

    def initUI(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()

        # Checkboxes for log levels
        checkbox_layout = QHBoxLayout()
        self.view_var = QCheckBox("View")
        self.view_var.setChecked(True)
        self.view_var.stateChanged.connect(self.filter_logs)
        checkbox_layout.addWidget(self.view_var)

        self.error_var = QCheckBox("Error")
        self.error_var.setChecked(True)
        self.error_var.stateChanged.connect(self.filter_logs)
        checkbox_layout.addWidget(self.error_var)

        self.warning_var = QCheckBox("Warning")
        self.warning_var.setChecked(True)
        self.warning_var.stateChanged.connect(self.filter_logs)
        checkbox_layout.addWidget(self.warning_var)

        self.info_var = QCheckBox("Info")
        self.info_var.setChecked(True)
        self.info_var.stateChanged.connect(self.filter_logs)
        checkbox_layout.addWidget(self.info_var)

        main_layout.addLayout(checkbox_layout)

        # Text widget for displaying logs
        self.text = QTextEdit()
        self.text.setFont(QFont("Courier", 10))
        self.text.setReadOnly(True)
        main_layout.addWidget(self.text)

        # Buttons
        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Logs")
        load_button.clicked.connect(self.load_logs)
        button_layout.addWidget(load_button)

        timeline_button = QPushButton("Show Timeline")
        timeline_button.clicked.connect(self.show_timeline)
        button_layout.addWidget(timeline_button)

        search_button = QPushButton("Search Online")
        search_button.clicked.connect(self.search_online)
        button_layout.addWidget(search_button)

        main_layout.addLayout(button_layout)

        # Canvas for timeline
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        main_layout.addWidget(self.canvas)

        main_widget.setLayout(main_layout)

    def load_logs(self):
        options = QFileDialog.Options()
        files, _ = QFileDialog.getOpenFileNames(self, "Open Log Files", "", "Log Files (*.log);;All Files (*)", options=options)
        self.logs = []
        for file_path in files:
            try:
                with open(file_path, 'r') as file:
                    self.logs.extend(file.readlines())
                print(f"Loaded {len(self.logs)} lines from {file_path}")
            except Exception as e:
                print(f"Error loading file {file_path}: {str(e)}")

        if not self.logs:
            QMessageBox.critical(self, "Error", "No logs were loaded. Please check the files and try again.")
            return

        self.logs.sort(key=self.extract_timestamp)
        self.filter_logs()

    def filter_logs(self):
        self.filtered_logs = []
        for log in self.logs:
            log_level = self.get_log_level(log)
            if (self.view_var.isChecked() and log_level == "View") or \
               (self.error_var.isChecked() and log_level == "Error") or \
               (self.warning_var.isChecked() and log_level == "Warning") or \
               (self.info_var.isChecked() and log_level == "Info"):
                self.filtered_logs.append(log)

        print(f"Filtered logs: {len(self.filtered_logs)}")
        self.display_logs()

    def display_logs(self):
        self.text.clear()
        for log in self.filtered_logs:
            log_level = self.get_log_level(log)
            if log_level == "Error":
                self.text.setTextColor(Qt.red)
            elif log_level == "Warning":
                self.text.setTextColor(Qt.darkYellow)
            elif log_level == "Info":
                self.text.setTextColor(Qt.blue)
            else:
                self.text.setTextColor(Qt.black)
            self.text.append(log)

        print(f"Displayed {self.text.document().blockCount()} lines")

    def extract_timestamp(self, log):
        match = re.search(r'\[(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2}\.\d{3})\]', log)
        if match:
            try:
                timestamp = datetime.strptime(match.group(1), '%d.%m.%Y %H:%M:%S.%f')
                if 1 <= timestamp.year <= 9999:
                    return timestamp
                else:
                    raise ValueError(f"Invalid year: {timestamp.year}")
            except ValueError as e:
                print(f"Error parsing timestamp: {match.group(1)} - {e}")
        return datetime.min

    def get_log_level(self, log):
        if re.search(r'\bWarning\b', log, re.IGNORECASE):
            return "Warning"
        elif re.search(r'\bError\b', log, re.IGNORECASE):
            return "Error"
        elif re.search(r'\bInfo\b', log, re.IGNORECASE):
            return "Info"
        else:
            return "View"

    def show_timeline(self):
        if not self.filtered_logs:
            QMessageBox.information(self, "Info", "No logs to display in timeline.")
            return

        timestamps = {'Error': [], 'Warning': [], 'Info': []}
        for log in self.filtered_logs:
            timestamp = self.extract_timestamp(log)
            log_level = self.get_log_level(log)
            if log_level in timestamps:
                timestamps[log_level].append(timestamp)

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        colors = {'Error': 'red', 'Warning': 'orange', 'Info': 'blue'}

        bins = 30  
        alpha = 1.0 

        for level in ['Error', 'Warning', 'Info']:
            if timestamps[level]:
                ax.hist(timestamps[level], bins=bins, color=colors[level], alpha=alpha, label=level)

        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title('Log Events Over Time')
        ax.legend()
        self.canvas.draw()

    def search_online(self):
        cursor = self.text.textCursor()
        if cursor.hasSelection():
            selected_text = cursor.selectedText()
            search_query = f"Veeam {selected_text}"
            webbrowser.open(f"https://www.google.com/search?q={search_query}")
        else:
            QMessageBox.information(self, "Info", "Please select an error description to search online.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LogAnalyzerApp()
    window.show()
    sys.exit(app.exec_())
