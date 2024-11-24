from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout

from View.LeftPanel.base_widget import BaseWidget


class PlatformDropdownMenu(BaseWidget):
    def __init__(self, view_model):
        super().__init__(view_model)

    def initialize_widgets(self):
        self.platform_label = QLabel("Platform:")
        self.platform_dropdown = QComboBox(self)

        self.platform_dropdown.addItems(self.view_model.data_manager.get_data('platforms', {}).keys())
        self.platform_dropdown.setCurrentText(self.view_model.data_manager.get_data('last_platform'))

        # Platform dropdown and recursive checkbox
    def configure_layout(self, layout):
        layout.addWidget(self.platform_label)
        layout.addWidget(self.platform_dropdown)