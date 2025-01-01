

from View.configuration_window.config_view import ConfigView


class ConfigWindowViewModel:

    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.config_window = ConfigView(self)

    def open_config_window(self):
        return self.config_window.open_config()

    def get_platform_list(self):
        return self.data_manager.get_data("platforms", {}).keys()

    def add_platform(self, platform):
        self.data_manager.set_data("platforms", platform)

    def delete_platform(self, platform):
        self.data_manager.delete_data("platforms", platform)