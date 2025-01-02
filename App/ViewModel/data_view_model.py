from PyQt5.QtCore import QObject, pyqtSignal


class DataViewModel(QObject):
    data_changed = pyqtSignal(str)

    def __init__(self, config_manager):
        super().__init__()
        self._config_manager = config_manager

    def get_data(self, key, subkey=None, default=None):
        return self._config_manager.get(key, subkey, default)

    def set_data(self, key, value, subkey=None, sub_value=None):
        self._config_manager.set(key, value, subkey, sub_value)
        self.data_changed.emit(str(key))

    def delete_data(self, key, subkey):
        self._config_manager.delete(key, subkey)
        self.data_changed.emit(str(key))

    def announce_change(self, data):
        self.data_changed.emit(str(data))
