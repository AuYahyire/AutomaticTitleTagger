from PyQt5.QtWidgets import QPushButton

from View.LeftPanel.base_widget import BaseWidget


class ExecuteStopButtons(BaseWidget):
    def __init__(self,view_model):
        super().__init__(view_model)

    def initialize_widgets(self):
        self.run_button = QPushButton("Ejecutar Titulador")
        self.stop_button = QPushButton("Detener")

    def configure_layout(self, layout):
        self.stop_button.setEnabled(False)
        layout.addWidget(self.run_button)
        layout.addWidget(self.stop_button)
