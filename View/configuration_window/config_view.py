from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QApplication, QDialog
)

from View.configuration_window.allowed_extensions import AllowedExtensions
from View.configuration_window.platform_details_window import PlatformDetailsWindow
from View.configuration_window.platform_dropdown import PlatformDropdown


class ConfigView(QDialog):
    def __init__(self, config_view_model):
        super().__init__()
        self.config_view_model = config_view_model
        self.setWindowTitle("Configuración")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()
        self.setup_components(layout)
        self.setLayout(layout)

    def setup_components(self, layout):
        layout.addLayout(self.create_api_key_field())
        layout.addWidget(AllowedExtensions(self.config_view_model))
        layout.addWidget(PlatformDropdown(self.config_view_model))
        layout.addWidget(PlatformDetailsWindow(self.config_view_model))

    def create_api_key_field(self):
        api_row = QHBoxLayout()
        text = QLabel("OpenAI API Key:")
        input_field = QLineEdit()
        input_field.setEchoMode(QLineEdit.Password)
        input_field.setText(self.config_view_model.get_api())
        api_row.addWidget(text)
        api_row.addWidget(input_field)

        input_field.textChanged.connect(self.config_view_model.set_api)

        return api_row

    def open_config(self):
        # Center the dialog on the screen
        screen = QApplication.primaryScreen().geometry()
        dialog_size = self.sizeHint()

        x = (screen.width() - dialog_size.width()) // 2
        y = (screen.height() - dialog_size.height()) // 2

        self.move(x, y)
        self.setModal(True)
        return self.exec_()









