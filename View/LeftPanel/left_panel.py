from PyQt5.QtWidgets import QVBoxLayout, QLayout, QWidget
from PyQt5.QtCore import pyqtSignal


class LeftPanel(QWidget):
    on_click_listener = pyqtSignal()

    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setup_ui()

    def setup_ui(self):
        left_layout = QVBoxLayout()
        left_layout.setContentsMargins(10, 10, 10, 10)
        left_layout.setSpacing(10)

        # Adding widgets and layouts to the left_layout
        widgets_and_layouts = [
            self.view_model.view_model_container.directory_widget,
            self.view_model.view_model_container.platform_dropdown_menu,
            self.view_model.view_model_container.progress_info_label,
            self.view_model.view_model_container.execution_buttons,
            self.view_model.view_model_container.status_dialog_bar,
        ]

        for item in widgets_and_layouts:
            if isinstance(item, QLayout):
                left_layout.addLayout(item)
            else:
                left_layout.addWidget(item)

        self.setLayout(left_layout)  # Establecer left_layout como el layout principal
        self.setMinimumSize(300, 400)
