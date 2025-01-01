from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtWidgets import QListView, QFileSystemModel, QWidget, QVBoxLayout, QAbstractItemView


class FileView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.layout = QVBoxLayout(self)

        # Obtener las extensiones permitidas desde data_view_model
        self.allowed_extensions = self.view_model.data_manager.get_data('allowed_extensions')

        # Configurar el modelo de sistema de archivos
        self.model = QFileSystemModel()
        self.model.setNameFilters([f"*.{ext}" for ext in self.allowed_extensions])  # Filtrar por extensiones
        self.model.setNameFilterDisables(False)  # Habilitar el filtro en el modelo


        # Configurar la vista de lista
        self.list_view = QListView()
        self.list_view.setMinimumSize(300, 400)  # Establecer un tamaño mínimo para la vista de lista
        self.setup_ui()

        # Conectar la señal directory_changed a auto_update_view
        self.view_model.directory_view_model.directory_changed.connect(self.auto_update_view)

    def setup_ui(self):
        """Inicializa la vista de archivos y conecta eventos"""
        # Obtener el directorio inicial del view_model o del data_view_model
        initial_directory = self.view_model.directory_view_model.current_directory or self.view_model.data_manager.get_data(
            'last_directory', '')

        # Establecer la ruta raíz
        self.model.setRootPath(initial_directory)
        self.list_view.setModel(self.model)
        self.list_view.setRootIndex(self.model.index(initial_directory))  # Establecer el índice raíz

        # Conectar el cambio de selección a la función que carga la imagen seleccionada
        self.list_view.selectionModel().selectionChanged.connect(self.on_item_selected)

        # Añadir la lista de archivos al diseño
        self.layout.addWidget(self.list_view)
        self.setLayout(self.layout)
        self.setMinimumSize(320, 450)  # Establecer un tamaño mínimo para el widget

    def on_item_selected(self, selected, deselected):
        """Evento al seleccionar un archivo, actualiza la imagen en la vista"""
        index = self.list_view.selectionModel().currentIndex()
        file_path = self.model.filePath(index)
        if file_path:
            self.view_model.directory_view_model.update_selected_file(
                file_path)  # Actualiza el archivo seleccionado en el modelo

    @pyqtSlot(str)
    def auto_update_view(self, directory):
        """Actualiza la vista de archivos cuando cambia el directorio"""
        self.model.setRootPath(directory)
        self.list_view.setRootIndex(self.model.index(directory))

