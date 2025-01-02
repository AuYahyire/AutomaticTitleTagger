from PyQt5.QtCore import QObject

from App.ViewModel.config_window_view_model import ConfigWindowViewModel
from App.ViewModel.data_view_model import DataViewModel
from App.ViewModel.directory_view_model import DirectoryViewModel
from App.ViewModel.logic_view_model import LogicViewModel
from App.ViewModel.view_model_container import ViewModelContainer
from Data.env_manager import EnvManager


class MainViewModel(QObject):
    def __init__(self, config_manager):
        super().__init__()
        self.env_manager = EnvManager()
        self.data_manager = DataViewModel(config_manager)
        self.directory_view_model = DirectoryViewModel(self.data_manager)
        self.logic_view_model = LogicViewModel(self.data_manager, self.env_manager)
        self.config_window_view_model = ConfigWindowViewModel(self.data_manager, self.env_manager)
        self.view_model_container = ViewModelContainer(self)
