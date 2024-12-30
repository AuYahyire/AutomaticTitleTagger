from PyQt5.QtCore import QLine
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QCheckBox, QComboBox, QGroupBox, \
    QPushButton, QApplication, QStyle


class ConfigView(QWidget):

    def __init__(self, view_model):
        super().__init__()
        self.config_view_model = view_model
        self.setWindowTitle("Configuración")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()
        self.config_window_components(layout)

        self.setLayout(layout)


    def config_window_components(self, layout):
        layout.addLayout(self.api_key_fieldtext())
        layout.addLayout(self.allowed_extensions())
        layout.addLayout(self.platforms_edit_dropdown())
        layout.addWidget(self.platform_details_window())

    def open_config(self):
        self.show()

    def api_key_fieldtext(self):
        api_row = QHBoxLayout()
        text = QLabel("OpenAI API Key:")
        input_field = QLineEdit()

        api_row.addWidget(text)
        api_row.addWidget(input_field)
        return api_row

    def allowed_extensions(self):
        ext_row = QHBoxLayout()
        allowed_extensions_checkbox = {
            QCheckBox(".jpeg"),
            QCheckBox(".jpg"),
            QCheckBox(".png"),
        }
        text = QLabel("Allowed Extensions:")
        ext_row.addWidget(text)
        for checkbox in allowed_extensions_checkbox:
            ext_row.addWidget(checkbox)

        return ext_row

    def platforms_edit_dropdown(self):
        platform_row = QHBoxLayout()
        text = QLabel("Platforms:")
        dropdown = QComboBox()
        platforms = self.config_view_model.get_platform_list() or []
        for platform in platforms:
            dropdown.addItem(platform)

        #

        platform_row.addWidget(text)
        platform_row.addWidget(dropdown)


        return platform_row

    def platform_details_window(self):
        detail_group_box = QGroupBox("Platform prompts:")
        detail_layout = QVBoxLayout()

        #Cada fila donde aparecen los prompts de la plataforma elegida
        system_row = QHBoxLayout()
        user_row = QHBoxLayout()

        #System prompt
        system_text = QLabel("System prompt:")
        system_value = QLabel()
        edit_system_text_button = QPushButton("...")
        edit_system_text_button.setFixedSize(20, 20)
        system_row.addWidget(system_text)
        system_row.addWidget(system_value)
        system_row.addWidget(edit_system_text_button)

        #User prompt
        user_text = QLabel("User prompt:")
        user_value = QLabel()
        edit_user_text_button = QPushButton("...")
        edit_user_text_button.setFixedSize(20, 20)
        user_row.addWidget(user_text)
        user_row.addWidget(user_value)
        user_row.addWidget(edit_user_text_button)

        #Construyó el layout
        detail_layout.addLayout(system_row)
        detail_layout.addLayout(user_row)

        #Aquí cierro el box.
        detail_group_box.setLayout(detail_layout)


        return detail_group_box
