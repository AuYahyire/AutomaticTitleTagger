from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
class ImageViewer(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setup_ui()

        # Conectar la señal file_selected a display_image
        self.view_model.directory_manager.file_selected.connect(self.display_image)

    def setup_ui(self):
        """Configura la interfaz para visualizar la imagen"""
        self.layout = QVBoxLayout()
        self.image_label = QLabel("No hay imagen seleccionada")  # Muestra la imagen
        self.image_label.setFixedSize(600, 500)  # Establece un tamaño fijo para la imagen
        self.name_label = QLabel("Nombre del archivo")  # Muestra el nombre del archivo

        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.name_label)
        self.setLayout(self.layout)

    def display_image(self, file_path):
        """Actualiza la interfaz con la imagen y su nombre"""
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.name_label.setText(file_path)
        else:
            self.image_label.setText('No se pudo cargar la imagen.')
            self.name_label.setText('')

