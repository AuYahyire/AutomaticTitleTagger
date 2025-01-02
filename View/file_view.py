from PyQt5.QtCore import pyqtSlot, QDir
from PyQt5.QtWidgets import QListView, QFileSystemModel, QWidget, QVBoxLayout, QAbstractItemView

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QListView
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileSystemModel


class FileView(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.layout = QVBoxLayout(self)

        # Initialize the model
        self.model = QFileSystemModel()
        self.model.setNameFilterDisables(False)  # Enable filter

        # Update filters initially
        self.update_allowed_extensions()

        # Setup list view
        self.list_view = QListView()
        self.list_view.setMinimumSize(300, 400)
        self.list_view.setModel(self.model)

        self.setup_ui()

        # Connect signals
        self.view_model.directory_view_model.directory_changed.connect(self.auto_update_view)
        self.view_model.data_manager.data_changed.connect(self.allowed_extensions_changed)

    def update_allowed_extensions(self):
        """Update the model's filters based on allowed extensions"""
        self.allowed_extensions = self.view_model.data_manager.get_data('allowed_extensions', [])
        # Create filters with wildcards
        filters = [f"*.{ext.lstrip('.')}" for ext in self.allowed_extensions]
        self.model.setNameFilters(filters)

    def setup_ui(self):
        """Initialize the file view and connect events"""
        initial_directory = (self.view_model.directory_view_model.current_directory or
                             self.view_model.data_manager.get_data('last_directory', ''))

        self.model.setRootPath(initial_directory)
        self.list_view.setRootIndex(self.model.index(initial_directory))

        # Connect selection change
        self.list_view.selectionModel().selectionChanged.connect(self.on_item_selected)

        # Add to layout
        self.layout.addWidget(self.list_view)
        self.setLayout(self.layout)
        self.setMinimumSize(320, 450)

    def on_item_selected(self, selected, deselected):
        """Handle file selection"""
        index = self.list_view.selectionModel().currentIndex()
        file_path = self.model.filePath(index)
        if file_path:
            self.view_model.directory_view_model.update_selected_file(file_path)

    @pyqtSlot(str)
    def auto_update_view(self, directory):
        """Update view when directory changes"""
        self.model.setRootPath(directory)
        self.list_view.setRootIndex(self.model.index(directory))

    def allowed_extensions_changed(self):
        """Handle changes in allowed extensions"""
        self.update_allowed_extensions()
        # Refresh the current view
        current_directory = (self.view_model.directory_view_model.current_directory or
                             self.view_model.data_manager.get_data('last_directory', ''))
        self.auto_update_view(current_directory)

    # TODO: Implementar navegación por carpetas en vista de archivos.
