from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox


class DirectoryWidget(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.directory_label = QLabel("Images directory")
        self.directory_input = QLineEdit(self)
        self.browse_button = QPushButton("Explore")
        self.recursive_checkbox = QCheckBox("Recursive?", self)

        self.setup_ui()

        # Conectar la señal directory_changed a update_directory
        self.view_model.directory_manager.directory_changed.connect(self.update_directory)

    def setup_ui(self):
        layout = QVBoxLayout()
        self.directory_input.setText(self.view_model.data_manager.get_data('last_directory'))
        self.browse_button.setFont(QFont('Times', 12))
        self.browse_button.clicked.connect(self.open_directory)

        self.recursive_checkbox.setChecked(self.view_model.data_manager.get_data("recursive", False))

        # Añadir widgets al layout
        layout.addWidget(self.directory_label)
        layout.addWidget(self.directory_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.recursive_checkbox)

        self.setLayout(layout)  # Establecer el layout principal

    def update_directory(self, directory):
        self.directory_input.setText(directory)

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory")
        if directory:
            self.view_model.data_manager.set_data('last_directory', directory)
            self.view_model.directory_manager.set_directory(directory)

