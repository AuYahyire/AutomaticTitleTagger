from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QMainWindow

from View.LeftPanel.left_panel import ButtonsLeftPanel
from View.file_view import FileView
from View.image_viewer import ImageViewer

class TituladorApp(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.setWindowFlags(Qt.Window | Qt.WindowMinimizeButtonHint | Qt.WindowCloseButtonHint)
        self.setWindowIcon(QIcon('/res/icon.png'))
        self.setWindowTitle("Configurador de Titulador")
        self.setGeometry(1450, 800, 1000, 500)
        self.setFixedSize(1000, 600)

        self.view_model = view_model
        self.data_manager = view_model.data_manager

        # Configura los componentes principales de la interfaz
        self.buttons_left_panel = ButtonsLeftPanel(self.view_model)
        self.file_view = FileView(self.view_model)
        self.image_viewer = ImageViewer(self.view_model)

        # Configura la interfaz principal
        self.setup_ui()

    def setup_ui(self):
        """Configura el diseño principal de la aplicación"""
        # Main layout setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)




        # Agrega los componentes al diseño
        main_layout.addWidget(self.buttons_left_panel)
        main_layout.addWidget(self.file_view)
        main_layout.addWidget(self.image_viewer)

        # Load stylesheet
        self.setStyleSheet(self.load_styles())

    def load_styles(self):
        """Load QSS style settings from file for maintainability."""
        return """
            QWidget { background-color: #2E3440; color: #D8DEE9; font-family: Arial; }
            QLabel { font-size: 16px; }
            QPushButton { background-color: #4C566A; border: 1px solid #D8DEE9; padding: 5px; }
            QPushButton:hover { background-color: #5E81AC; }
            QPushButton:pressed { background-color: #45a049; }
            QLineEdit, QComboBox, QCheckBox { background-color: #3B4252; border: 1px solid #D8DEE9; padding: 5px; }
            QProgressBar::chunk { background-color: #4CAF50; }
        """
