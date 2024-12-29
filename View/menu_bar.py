from PyQt5.QtWidgets import QMenuBar, QAction


class MenuBar:
    def __init__(self, titulador_app):
        self.main_window = titulador_app

        self.menu_bar = QMenuBar()
        self.setup_menu_bar()


    def setup_menu_bar(self):
        # Crear menu
        file_menu_bar = self.menu_bar.addMenu("Archivo")
        about_menu_bar = self.menu_bar.addMenu("Acerca de...")

        # Aquí añado acciones a los menus
        about_action = QAction("Acerca de esta aplicación", self.main_window)
        about_action.triggered.connect(self.open_config)  # Conectar evento
        about_menu_bar.addAction(about_action)

        config_action = QAction("Configuración", self.main_window)
        config_action.triggered.connect(self.open_config)  # Conectar acción
        file_menu_bar.addAction(config_action)  # Aqui se añaden a la barra

    def open_config(self):
        self.main_window.view_model.view_model_container.config_window.open_config()

