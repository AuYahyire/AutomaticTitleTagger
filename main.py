# main.py
from Data import enums
from Data.json_manager import JsonManager, DEFAULT_CONFIGURATION
from App.app_launcher import AppLauncher

def main():
    config_manager = JsonManager(enums.ConfigFiles.CONFIG.value, DEFAULT_CONFIGURATION)
    app_launcher = AppLauncher(config_manager)
    app_launcher.run()

if __name__ == "__main__":
    main()

# TODO: Unificar idiomas o añadir alternativas.
# TODO: Cambiar prints por Logs y añadir más logs.
# TODO: Crear más pruebas unitarias y acomodar la logica de las fallidas.
# TODO: Añadir documentation comments.