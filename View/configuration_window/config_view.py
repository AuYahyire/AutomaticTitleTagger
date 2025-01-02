from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QHBoxLayout, QLineEdit, QCheckBox, QComboBox,
    QGroupBox, QPushButton, QApplication, QDialog, QMessageBox
)

PIXEL_SIZE = 25


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



class PlatformDropdown(QWidget):
    def __init__(self, config_view_model):
        super().__init__()
        self.config_view_model = config_view_model
        layout = QHBoxLayout()
        self.setup_components(layout)
        self.setLayout(layout)

    def setup_components(self, layout):
        text = QLabel("Platforms:")
        self.dropdown = QComboBox()
        self.update_dropdown()

        add_button = self.create_button("A", "Add a new platform", self.add_new_platform)
        delete_button = self.create_button("D", "Delete the selected platform", self.delete_platform)

        layout.addWidget(text)
        layout.addWidget(self.dropdown)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)

    def create_button(self, label, tooltip, action):
        button = QPushButton(label)
        button.setToolTip(tooltip)
        button.setFixedSize(PIXEL_SIZE, PIXEL_SIZE)
        button.clicked.connect(action)
        return button

    def add_new_platform(self):
        platform_name = self.show_input_dialog("Añadir plataforma", "Nombre de la plataforma:")
        if platform_name:
            self.config_view_model.add_platform(platform_name)
            self.dropdown.addItem(platform_name)

    def update_dropdown(self):
        self.dropdown.clear()
        self.dropdown.addItems(self.config_view_model.get_platform_list() or [])

    def delete_platform(self):
        platform = self.dropdown.currentText()
        if self.show_confirmation_dialog("Eliminar plataforma", "¿Está seguro?"):
            self.config_view_model.delete_platform(platform)
            self.dropdown.removeItem(self.dropdown.currentIndex())

    def show_input_dialog(self, title, label):
        dialog = QDialog(self)
        dialog.setWindowTitle(title)
        layout = QVBoxLayout()
        input_field = QLineEdit()
        layout.addWidget(QLabel(label))
        layout.addWidget(input_field)
        button = QPushButton("Aceptar")
        button.clicked.connect(dialog.accept)
        layout.addWidget(button)
        dialog.setLayout(layout)
        if dialog.exec_() == QDialog.Accepted:
            return input_field.text().strip()
        return None

    def show_confirmation_dialog(self, title, message):
        reply = QMessageBox.question(self, title, message, QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes


class PlatformDetailsWindow(QGroupBox):
    def __init__(self, view_model):
        super().__init__("Platform prompts:")
        self.view_model = view_model
        layout = QVBoxLayout()
        self.setup_components(layout)
        self.setLayout(layout)

    def setup_components(self, layout):
        layout.addLayout(self.create_prompt_row("System prompt:"))
        layout.addLayout(self.create_prompt_row("User prompt:"))

    def create_prompt_row(self, label_text):
        row = QHBoxLayout()
        text = QLabel(label_text)
        value = QLabel()
        edit_button = QPushButton("...")
        edit_button.setFixedSize(PIXEL_SIZE, PIXEL_SIZE)
        row.addWidget(text)
        row.addWidget(value)
        row.addWidget(edit_button)
        return row


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