from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout

from View.LeftPanel.base_widget import BaseWidget


class PlatformDropdownMenu(BaseWidget):
    def __init__(self, view_model):
        super().__init__(view_model)
        self.view_model.data_manager.data_changed.connect(self.update_dropdown)

    def initialize_widgets(self):
        self.platform_label = QLabel("Platform:")
        self.platform_dropdown = QComboBox(self)

        self.update_dropdown()

        self.view_model.data_manager.set_data('last_platform', self.platform_dropdown.currentText())
        self.platform_dropdown.setCurrentText(self.view_model.data_manager.get_data('last_platform'))

        # Platform dropdown and recursive checkbox
    def configure_layout(self, layout):
        layout.addWidget(self.platform_label)
        layout.addWidget(self.platform_dropdown)

    def update_dropdown(self):
        self.platform_dropdown.clear()
        self.platform_dropdown.addItems(self.view_model.data_manager.get_data('platforms', {}).keys())