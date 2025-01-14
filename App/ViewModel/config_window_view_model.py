from PyQt5.QtCore import pyqtSignal, QObject

from View.configuration_window.config_view import ConfigView


class ConfigWindowViewModel(QObject):
    platform_changed = pyqtSignal(str)

    def __init__(self, data_manager, env_manager):
        super().__init__()
        self.data_manager = data_manager
        self.env_manager = env_manager
        self.config_window = ConfigView(self)

    def open_config_window(self):
        return self.config_window.open_config()

    def get_platform_list(self):
        return self.data_manager.get_data("platforms", {}).keys()

    def add_platform(self, platform):
        self.data_manager.set_data("platforms", platform)

    def delete_platform(self, platform):
        self.data_manager.delete_data("platforms", platform)

    def get_api(self):
        return self.env_manager.get_api_key("OPENAI_API_KEY")

    def set_api(self, api):
        self.env_manager.set_api_key("OPENAI_API_KEY", api)

    def get_allowed_extensions(self):
        return self.data_manager.get_data("allowed_extensions")

    def set_allowed_extensions(self, extension):
        self.data_manager.set_data("allowed_extensions", extension)

    def get_platform_prompts(self, platform, text):
        return self.data_manager.get_data("platforms", platform, text)

    def set_platform_prompts(self, platform, text, value):
        self.data_manager.set_data("platforms", platform, text, value)