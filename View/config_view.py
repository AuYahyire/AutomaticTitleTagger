from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit


class ConfigView(QWidget):

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setWindowTitle("Configuración")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()
        self.config_window_components(layout)

        self.setLayout(layout)

    def config_window_components(self, layout):
        layout.addLayout(self.api_key_fieldtext())

    def open_config(self):
        self.show()

    def api_key_fieldtext(self):
        field = QHBoxLayout()
        text = QLabel("OpenAI API Key:")
        input_field = QLineEdit()

        field.addWidget(text)
        field.addWidget(input_field)
        return field

    def allowed_extensions(self):
        field = QHBoxLayout()

