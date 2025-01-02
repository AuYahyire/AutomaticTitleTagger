from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel, QComboBox, QPushButton, QDialog, QVBoxLayout, QLineEdit, \
    QMessageBox

PIXEL_SIZE = 25

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

        self.dropdown.currentTextChanged.connect(self.on_platform_changed)

        layout.addWidget(text)
        layout.addWidget(self.dropdown)
        layout.addWidget(add_button)
        layout.addWidget(delete_button)

    def on_platform_changed(self, platform):
        self.config_view_model.platform_changed.emit(platform)
        print(f"Platform changed to: {platform}")

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