from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy

from View.LeftPanel.base_widget import BaseWidget


class ProgressInfoLabel(BaseWidget):

    def __init__(self, view_model):
        super().__init__(view_model)

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



