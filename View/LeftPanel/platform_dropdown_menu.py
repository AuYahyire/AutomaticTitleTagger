from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout


class PlatformDropdownMenu(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.platform_label = QLabel("Platform:")
        self.platform_dropdown = QComboBox(self)
        self.setup_ui()

        # Platform dropdown and recursive checkbox
    def setup_ui(self):
        layout = QVBoxLayout()

        self.platform_dropdown.addItems(self.view_model.data_manager.get_data('platforms', {}).keys())
        self.platform_dropdown.setCurrentText(self.view_model.data_manager.get_data('last_platform'))

        layout.addWidget(self.platform_label)
        layout.addWidget(self.platform_dropdown)
        self.setLayout(layout)