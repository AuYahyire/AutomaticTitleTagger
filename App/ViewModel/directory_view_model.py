from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

class DirectoryViewModel(QObject):
    directory_changed = pyqtSignal(str)
    file_selected = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.current_directory = ""
        self.current_file = ""

    def set_directory(self, directory):
        self.current_directory = directory
        self.directory_changed.emit(directory)

    @pyqtSlot(str)
    def update_selected_file(self, file_path):
        self.current_file = file_path
        self.file_selected.emit(file_path)

