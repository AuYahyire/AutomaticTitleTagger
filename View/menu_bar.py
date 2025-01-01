from PyQt5.QtWidgets import QMenuBar, QAction

from View.configuration_window.config_view import ConfigView


class MenuBar:
    def __init__(self, view_model):
        self.view_model = view_model

        self.menu_bar = QMenuBar()
        self.setup_menu_bar()


    def setup_menu_bar(self):
        # Crear menu
        file_menu_bar = self.menu_bar.addMenu("Archivo")
        about_menu_bar = self.menu_bar.addMenu("Acerca de...")

        # Aquí añado acciones a los menus
        about_action = QAction("Acerca de esta aplicación", self.view_model)
        about_action.triggered.connect(self.open_config)  # Conectar evento
        about_menu_bar.addAction(about_action)

        config_action = QAction("Configuración", self.view_model)
        config_action.triggered.connect(self.open_config)  # Conectar acción
        file_menu_bar.addAction(config_action)  # Aqui se añaden a la barra

    def open_config(self):
        self.view_model.config_window_view_model.open_config_window()


