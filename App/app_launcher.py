import sys
from PyQt5.QtWidgets import QApplication

from App.ViewModel.main_view_model import MainViewModel
from View.titulador_app import TituladorApp
#from App.ui.ui import TituladorApp


class AppLauncher:
    def __init__(self, config_manager):
        self.config_manager = config_manager

    def run(self):
        app = QApplication(sys.argv)
        view_model = MainViewModel(self.config_manager)
        titulador_app = TituladorApp(view_model)
        titulador_app.show()
        sys.exit(app.exec_())
