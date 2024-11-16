from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy


class ProgressInfoLabel(QWidget):

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.progress_bar = QProgressBar(self)
        self.file_label = QLabel('Archivo:')
        self.current_image_label = QLabel('')
        self.estimated_time_label = QLabel('')

        self.setup_ui()

    def setup_ui(self):
        self.setup_progress_bar()
        file_info_layout = self.setup_file_info()

        layout = QVBoxLayout()
        layout.addWidget(self.progress_bar)
        layout.addLayout(file_info_layout)

        self.setLayout(layout)

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



