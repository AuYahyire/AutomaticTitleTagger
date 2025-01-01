from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QFileDialog, QCheckBox

from View.LeftPanel.base_widget import BaseWidget

LAST_DIRECTORY_KEY = 'last_directory'

class DirectoryWidget(BaseWidget):
    def __init__(self, view_model):
        super().__init__(view_model)

    def initialize_widgets(self):
        self.directory_label = QLabel("Images directory")
        self.directory_input = QLineEdit(self)
        self.browse_button = QPushButton("Explore")
        self.recursive_checkbox = QCheckBox("Recursive?", self)

        # Conectar la señal directory_changed a update_directory
        self.view_model.directory_view_model.directory_changed.connect(self.update_directory)

    def configure_layout(self, layout):
        # Set initial values and properties
        self.directory_input.setText(self.view_model.directory_view_model.get(LAST_DIRECTORY_KEY))
        self.browse_button.setFont(QFont('Times', 12))
        self.recursive_checkbox.setChecked(self.view_model.directory_view_model.get_recursive_state())

        # Connect button click signal
        self.browse_button.clicked.connect(self.open_directory)
        # Connect checkbox state change signal
        self.recursive_checkbox.stateChanged.connect(self.update_recursive_setting)


        # Añadir widgets al layout
        layout.addWidget(self.directory_label)
        layout.addWidget(self.directory_input)
        layout.addWidget(self.browse_button)
        layout.addWidget(self.recursive_checkbox)

    def update_directory(self, directory):
        self.directory_input.setText(directory)

    def open_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select directory")
        if directory:
            self.view_model.directory_view_model.set(LAST_DIRECTORY_KEY, directory)

    def update_recursive_setting(self, state):
        self.view_model.directory_view_model.set_recursive_state(state)
