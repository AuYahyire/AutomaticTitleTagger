from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from torch import layout


class ExecuteStopButtons(QWidget):
    def __init__(self,view_model):
        super().__init__()
        self.view_model = view_model
        self.run_button = QPushButton("Ejecutar Titulador")
        self.stop_button = QPushButton("Detener")

        self.setup_ui()

    def setup_ui(self):
        self.run_button.setFont(QFont('Times', 12))
        self.stop_button.setFont(QFont('Times', 12))
        self.stop_button.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.run_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)
