# status bar
from PyQt5.QtWidgets import QWidget, QStatusBar, QVBoxLayout

from View.LeftPanel.base_widget import BaseWidget


class StatusDialogBar(BaseWidget):
    def __init__(self,view_model):
        super().__init__(view_model)

    def initialize_widgets(self):
        self.status_dialog_bar = QStatusBar()
        self.status_dialog_bar.showMessage("Status bar message.")

    def configure_layout(self, layout):
        layout.addWidget(self.status_dialog_bar)
