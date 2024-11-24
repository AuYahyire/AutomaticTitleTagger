from PyQt5.QtWidgets import QWidget, QVBoxLayout


class BaseWidget(QWidget):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        self.initialize_widgets()
        self.configure_layout(layout)
        self.setLayout(layout)

    def initialize_widgets(self):
        raise NotImplementedError("Subclasses should implement this method.")

    def configure_layout(self, layout):
        raise NotImplementedError("Subclasses should implement this method.")