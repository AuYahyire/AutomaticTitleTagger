from PyQt5.QtCore import QObject, pyqtSignal


class DataViewModel(QObject):
    data_changed = pyqtSignal(str)

    def __init__(self, config_manager):
        super().__init__()
        self._config_manager = config_manager

    def get_data(self, key, default=None):
        return self._config_manager.get(key, default)

    def set_data(self, key, value):
        self._config_manager.set(key, value)
        self.data_changed.emit(key)

    def delete_platform(self, key, subkey):
        self._config_manager.delete(key, subkey)
        self.data_changed.emit(key)
