from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, Qt



class DirectoryViewModel(QObject):
    directory_changed = pyqtSignal(str)
    file_selected = pyqtSignal(str)

    def __init__(self, data_view_model):
        super().__init__()
        self.current_directory = ""
        self.current_file = ""
        self.data_view_model = data_view_model

    def set(self, key, value):
        self.current_directory = value
        self.data_view_model.set_data(key, value)
        self.directory_changed.emit(value)

    def get(self, key):
        return self.data_view_model.get_data(key)


    def get_recursive_state(self):
        return self.data_view_model.get_data("recursive", False)

    def set_recursive_state(self, state):
        is_recursive = state == Qt.Checked
        self.data_view_model.set_data("recursive", is_recursive)

    @pyqtSlot(str)
    def update_selected_file(self, file_path):
        self.current_file = file_path
        self.file_selected.emit(file_path)

