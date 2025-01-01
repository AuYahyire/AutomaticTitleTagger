from PyQt5.QtCore import QLine, Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QCheckBox, QComboBox, QGroupBox, \
    QPushButton, QApplication, QStyle, QDialog, QMessageBox

PIXEL_SIZE = 25

class ConfigView(QDialog):

    def __init__(self, view_model):
        super().__init__()
        self.config_view_model = view_model
        self.setWindowTitle("Configuración")
        self.setGeometry(200, 200, 300, 200)

        layout = QVBoxLayout()
        self.config_window_components(layout)

        self.setLayout(layout)

        #Connect signal
        self.config_view_model

    def config_window_components(self, layout):
        layout.addLayout(self.api_key_fieldtext())
        layout.addLayout(self.allowed_extensions())
        layout.addLayout(self.platforms_dropdown())
        layout.addWidget(self.platform_details_window())

    def open_config(self):
        # Center the dialog on the screen
        screen = QApplication.primaryScreen().geometry()
        dialog_size = self.sizeHint()

        x = (screen.width() - dialog_size.width()) // 2
        y = (screen.height() - dialog_size.height()) // 2

        self.move(x, y)
        self.setModal(True)
        self.exec_()

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

    """
    A dropdown with all the platforms in the json config file, and with buttons to add, edit and delete.
    """

    def platforms_dropdown(self):
        platform_row = QHBoxLayout()

        # Label
        text = QLabel("Platforms:")

        # ComboBox setup
        dropdown = QComboBox()
        platforms = self.config_view_model.get_platform_list() or []
        dropdown.addItems(platforms)

        # Add Button
        add_button = QPushButton("A")
        add_button.setToolTip("Add a new platform")
        add_button.setFixedSize(PIXEL_SIZE, PIXEL_SIZE)
        add_button.clicked.connect(self.add_new_platform)


        # Delete Button
        delete_button = QPushButton("D")
        delete_button.setToolTip("Delete the selected platform")
        delete_button.setFixedSize(PIXEL_SIZE, PIXEL_SIZE)
        delete_button.clicked.connect(lambda: self.delete_platform(dropdown.currentText()))


        # Assemble the layout
        platform_row.addWidget(text)
        platform_row.addWidget(dropdown)
        platform_row.addWidget(add_button)
        platform_row.addWidget(delete_button)

        return platform_row

    """
    Square details window with system and user prompt, with buttons to edit them.
    """
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
        edit_system_text_button.setFixedSize(PIXEL_SIZE, PIXEL_SIZE)
        system_row.addWidget(system_text)
        system_row.addWidget(system_value)
        system_row.addWidget(edit_system_text_button)

        #User prompt
        user_text = QLabel("User prompt:")
        user_value = QLabel()
        edit_user_text_button = QPushButton("...")
        edit_user_text_button.setFixedSize(PIXEL_SIZE, PIXEL_SIZE)
        user_row.addWidget(user_text)
        user_row.addWidget(user_value)
        user_row.addWidget(edit_user_text_button)

        #Construyó el layout
        detail_layout.addLayout(system_row)
        detail_layout.addLayout(user_row)

        #Aquí cierro el box.
        detail_group_box.setLayout(detail_layout)


        return detail_group_box

    def add_new_platform(self):
        add_dialog = QDialog()
        add_dialog.setWindowTitle("Añadir plataforma")

        # Main layout
        layout = QVBoxLayout()

        # Platform name input
        input_layout = QHBoxLayout()
        input_label = QLabel("Nombre de la plataforma:")
        self.platform_input = QLineEdit()
        input_layout.addWidget(input_label)
        input_layout.addWidget(self.platform_input)
        layout.addLayout(input_layout)

        # Button layout
        button_layout = QHBoxLayout()
        accept_button = QPushButton("Aceptar")
        cancel_button = QPushButton("Cancelar")

        button_layout.addWidget(accept_button)
        button_layout.addWidget(cancel_button)
        layout.addLayout(button_layout)

        # Set layout
        add_dialog.setLayout(layout)

        # Button connections
        def on_accept():
            platform_name = self.platform_input.text().strip()
            if platform_name:
                add_dialog.accept()
            else:
                QMessageBox.warning(add_dialog, "Error", "El nombre de la plataforma no puede estar vacío")

        def on_cancel():
            add_dialog.reject()

        accept_button.clicked.connect(on_accept)
        cancel_button.clicked.connect(on_cancel)

        # Center and show dialog
        add_dialog.setModal(True)


        # Execute dialog
        result = add_dialog.exec_()

        # Handle result
        if result == QDialog.Accepted:
            self.config_view_model.add_platform(self.platform_input.text().strip())

    def delete_platform(self, platform):
        warning = QDialog()
        warning_layout = QVBoxLayout()
        warning_text = QLabel(
            "This will delete the platform and their system and user text, this can't be restored. Proceed?")

        # Button layout
        button_layout = QHBoxLayout()
        accept_button = QPushButton("Aceptar")
        cancel_button = QPushButton("Cancelar")

        button_layout.addWidget(accept_button)
        button_layout.addWidget(cancel_button)

        warning_layout.addWidget(warning_text)
        warning_layout.addLayout(button_layout)

        warning.setLayout(warning_layout)

        # Connect buttons directly
        accept_button.clicked.connect(warning.accept)
        cancel_button.clicked.connect(warning.reject)

        result = warning.exec_()

        if result == QDialog.Accepted:
            self.config_view_model.delete_platform(platform)

