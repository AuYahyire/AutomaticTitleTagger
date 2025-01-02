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
        self.run_button.clicked.connect(self.view_model.logic_view_model.initialize_execution)
        self.stop_button.clicked.connect(self.stop_execution)

        layout.addWidget(self.run_button)
        layout.addWidget(self.stop_button)

    # TODO: Implementar la lógica para detener la ejecución
    def stop_execution(self):
        pass
