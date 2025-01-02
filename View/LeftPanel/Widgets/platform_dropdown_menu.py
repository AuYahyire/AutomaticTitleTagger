from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QVBoxLayout

from View.LeftPanel.base_widget import BaseWidget


class PlatformDropdownMenu(BaseWidget):
    def __init__(self, view_model):
        self._updating = False  # Flag to prevent recursive updates
        super().__init__(view_model)
        self.view_model.data_manager.data_changed.connect(self.update_dropdown)

    def initialize_widgets(self):
        self.platform_label = QLabel("Platform:")
        self.platform_dropdown = QComboBox(self)

        # Update dropdown with initial items
        self.update_dropdown()

        # Set initial value from last_platform
        initial_platform = self.view_model.data_manager.get_data('last_platform')
        if initial_platform:
            self.platform_dropdown.setCurrentText(initial_platform)

        # Connect the signal to handle selection changes
        self.platform_dropdown.currentTextChanged.connect(self.on_platform_changed)

    def configure_layout(self, layout):
        layout.addWidget(self.platform_label)
        layout.addWidget(self.platform_dropdown)

    def update_dropdown(self):
        if self._updating:  # Prevent recursive updates
            return

        try:
            self._updating = True
            current_text = self.platform_dropdown.currentText()
            self.platform_dropdown.clear()
            platforms = self.view_model.data_manager.get_data('platforms', {}).keys()
            self.platform_dropdown.addItems(platforms)

            # Restore the previous selection if it still exists in the new items
            if current_text in platforms:
                self.platform_dropdown.setCurrentText(current_text)
        finally:
            self._updating = False
            print("Dropdown updated")

    def on_platform_changed(self, text):
        if self._updating:  # Prevent recursive updates
            return

        try:
            self._updating = True
            self.view_model.data_manager.set_data('last_platform', text)
        finally:
            self._updating = False
            print(f"Platform changed to: {text}")