from PyQt5.QtCore import QObject
from App.ViewModel.data_view_model import DataViewModel
from App.ViewModel.directory_view_model import DirectoryViewModel
from App.ViewModel.view_model_container import ViewModelContainer


class MainViewModel(QObject):
    def __init__(self, config_manager):
        super().__init__()
        self.data_manager = DataViewModel(config_manager)
        self.directory_manager = DirectoryViewModel()
        self.view_model_container = ViewModelContainer(self)
