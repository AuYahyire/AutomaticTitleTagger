from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCheckBox

PIXEL_SIZE = 25

class AllowedExtensions(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.checkboxes = []
        layout = QVBoxLayout()
        self.setup_components(layout)
        self.setLayout(layout)

    def setup_components(self, layout):
        available_extensions = ["jpeg", "jpg", "png"]  # Fixed list of options
        checked_extensions = self.view_model.get_allowed_extensions()  # Previously saved selections

        for extension in available_extensions:
            checkbox = QCheckBox(extension)
            # Set checked if this extension was previously selected
            if extension in checked_extensions:
                checkbox.setChecked(True)
            else:
                checkbox.setChecked(False)

            checkbox.stateChanged.connect(self.update_checked_extensions)
            self.checkboxes.append(checkbox)
            layout.addWidget(checkbox)

    def get_checked_extensions(self):
        """Returns a list of only the checked extensions"""
        return [
            checkbox.text()
            for checkbox in self.checkboxes
            if checkbox.isChecked()
        ]

    def update_checked_extensions(self):
        """Updates the view model with current checked extensions"""
        checked = self.get_checked_extensions()
        self.view_model.set_allowed_extensions(checked)