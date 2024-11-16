from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QComboBox, QCheckBox, QProgressBar, QHBoxLayout, \
    QSpacerItem, QSizePolicy, QStatusBar, QLayout, QWidget
from PyQt5.QtCore import pyqtSignal, Qt

from View.LeftPanel.directory_dialog.directory_widget import DirectoryWidget
from View.LeftPanel.platform_label.platform_dropdown_menu import PlatformDropdownMenu
from View.LeftPanel.progress_info.progress_info_labels import ProgressInfoLabel


class ButtonsLeftPanel(QWidget):
    on_click_listener = pyqtSignal()

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.directory = DirectoryWidget(self.view_model)
        self.platforms = PlatformDropdownMenu(self.view_model)
        self.progress_info = ProgressInfoLabel(self.view_model)
        self.setup_ui()

    def setup_ui(self):
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)


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
            self.progress_info,
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
