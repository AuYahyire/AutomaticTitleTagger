from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy

from View.LeftPanel.base_widget import BaseWidget


class ProgressInfoLabel(BaseWidget):

    def __init__(self, view_model):
        super().__init__(view_model)

        self.view_model.logic_view_model.progress_signal.connect(self.update_progress)

    def initialize_widgets(self):
        self.progress_bar = QProgressBar(self)
        self.file_label = QLabel('Archivo:')
        self.current_image_label = QLabel('')
        self.estimated_time_label = QLabel('')
        self.setup_progress_bar()

    def configure_layout(self, layout):
        file_info_layout = self.setup_file_info()
        layout.addWidget(self.progress_bar)
        layout.addLayout(file_info_layout)

    def setup_progress_bar(self):
        self.progress_bar.setValue(0)

    def setup_file_info(self):
        file_info_layout = QHBoxLayout()
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        file_info_layout.addWidget(self.file_label)
        file_info_layout.addSpacerItem(spacer)
        file_info_layout.addWidget(self.current_image_label)
        file_info_layout.addWidget(self.estimated_time_label)

        return file_info_layout

    @pyqtSlot(dict)  # Listen for dictionary signal
    def update_progress(self, progress_data):
        """Update the UI components based on the progress data."""
        self.progress_bar.setValue(progress_data['progress_percentage'])  # Update the progress bar
        self.file_label.setText(progress_data['current_file'])  # Update the file label
        self.current_image_label.setText(
            f"{progress_data['current_image_number']} / {progress_data['total_images']}")  # Update image counter
        self.estimated_time_label.setText(
            f"Tiempo estimado: {progress_data['remaining_time']:.2f} segundos")  # Update estimated time




