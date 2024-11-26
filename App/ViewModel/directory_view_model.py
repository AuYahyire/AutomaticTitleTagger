from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt


class DirectoryViewModel(QObject):
    directory_changed = pyqtSignal(str)
    file_selected = pyqtSignal(str)

    def __init__(self, data_manager):
        super().__init__()
        self.current_directory = ""
        self.current_file = ""
        self.data_manager = data_manager

    def update_directory(self, directory):
        self.current_directory = directory
        self.data_manager.set_data('last_directory', directory)
        self.directory_changed.emit(directory)

    def get_directory(self):
        return self.data_manager.get_data('last_directory')

    def get_recursive_state(self):
        return self.data_manager.get_data("recursive", False)

    def set_recursive_state(self, state):
        is_recursive = state == Qt.Checked
        self.data_manager.set_data("recursive", is_recursive)

    @pyqtSlot(str)
    def update_selected_file(self, file_path):
        self.current_file = file_path
        self.file_selected.emit(file_path)

