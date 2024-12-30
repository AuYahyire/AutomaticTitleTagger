

from View.config_view import ConfigView


class ConfigWindowViewModel():

    def __init__(self, data_manager):
        self.data_manager = data_manager
        self.config_window = ConfigView(self)

    def open_config_window(self):
        self.config_window.show()

    def get_platform_list(self):
        return self.data_manager.get_data("platforms")