from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox, QProgressBar, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QStatusBar, QLayout, QWidget
from PyQt5.QtCore import pyqtSignal, Qt

from View.LeftPanel.directory_dialog.directory_widget import DirectoryWidget
from View.LeftPanel.platform_label.platform_dropdown_menu import PlatformDropdownMenu


class ButtonsLeftPanel(QWidget):
    on_click_listener = pyqtSignal()

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.directory = DirectoryWidget(self.view_model)
        self.platforms = PlatformDropdownMenu(self.view_model)
        self.setup_ui()

    def setup_ui(self):
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)


        # Progress bar and control buttons
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        # Progress file info layout
        file_info_layout = QHBoxLayout()
        self.file_label = QLabel('Archivo:')
        self.current_image_label = QLabel('')
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        file_info_layout.addWidget(self.file_label)
        file_info_layout.addSpacerItem(spacer)
        file_info_layout.addWidget(self.current_image_label)

        # Estimated time label
        self.estimated_time_label = QLabel('')

        self.run_button = QPushButton("Ejecutar Titulador")
        self.run_button.setFont(QFont('Times', 12))

        self.stop_button = QPushButton("Detener")
        self.stop_button.setFont(QFont('Times', 12))
        self.stop_button.setEnabled(False)

        # status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Falta configurar el API!")

        # Adding widgets and layouts to the left_layout
        widgets_and_layouts = [
            self.directory,
            self.platforms,
            self.progress_bar,
            file_info_layout,  # Es un layout
            self.estimated_time_label,
            self.run_button,
            self.stop_button,
            self.status_bar
        ]

        for item in widgets_and_layouts:
            if isinstance(item, QLayout):
                left_layout.addLayout(item)
            else:
                left_layout.addWidget(item)

        self.setLayout(left_layout)  # Establecer left_layout como el layout principal
