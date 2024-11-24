# status bar
from PyQt5.QtWidgets import QWidget, QStatusBar, QVBoxLayout


class StatusDialogBar(QWidget):
    def __init__(self,view_model):
        super().__init__()
        self.view_model = view_model
        self.status_dialog_bar = QStatusBar()

        self.setup_ui()

    def setup_ui(self):
        self.status_dialog_bar.showMessage("Status bar message.")

        layout = QVBoxLayout()
        layout.addWidget(self.status_dialog_bar)

        self.setLayout(layout)