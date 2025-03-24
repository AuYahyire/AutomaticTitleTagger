import os
import time
from PyQt5.QtCore import QThread, pyqtSignal, pyqtSlot
from Logic.file_manager import FileManager


class ImageProcessorWorker(QThread):
    progress_signal = pyqtSignal(dict)
    break_signal = pyqtSignal()
    finished_signal = pyqtSignal()

    def __init__(self, image_folder, recursive, processor, allowed_extensions, user_text, system_text):
        super().__init__()
        self.image_folder = image_folder
        self.recursive = recursive
        self.processor = processor
        self.allowed_extensions = allowed_extensions
        self.user_text = user_text
        self.system_text = system_text
        self.is_running = False
        self.is_stopped = False

    def run(self):
        self.is_running = True
        total_images = self.count_total_images()


        if self.recursive:
            for root, _, files in os.walk(self.image_folder):
                folder_name = os.path.basename(root)
                filtered_image_files = FileManager.filter_image_files(files, self.allowed_extensions)
                if filtered_image_files:
                    all_image_files_path = [os.path.join(root, file) for file in filtered_image_files]
                    if self.process_images_to_csv(all_image_files_path, root, folder_name, total_images):
                        return
        else:
            root, _, files = next(os.walk(self.image_folder))
            folder_name = os.path.basename(root)
            filtered_image_files = FileManager.filter_image_files(files, self.allowed_extensions)
            if filtered_image_files:
                all_image_files_path = [os.path.join(root, file) for file in filtered_image_files]
                if self.process_images_to_csv(all_image_files_path, root, folder_name, total_images):
                    return

        self.finished_signal.emit()
        self.is_running = False

    def count_total_images(self):
        total_images = 0
        if self.recursive:
            for root, _, files in os.walk(self.image_folder):
                filtered_image_files = FileManager.filter_image_files(files, self.allowed_extensions)
                total_images += len(filtered_image_files)
        else:
            all_files = os.listdir(self.image_folder)
            filtered_image_files = FileManager.filter_image_files(all_files, self.allowed_extensions)
            total_images = len(filtered_image_files)
        return total_images

    def process_images_to_csv(self, all_image_files_path, root, folder_name, total_images):
        image_data = self.processor.process_image(all_image_files_path, self.system_text, self.user_text, total_images)
        if self.check_image_data(image_data):
            return True
        FileManager.create_csv(root, folder_name, image_data)

    def check_image_data(self, image_data):
        """Check if the image data is None and handle stopping the processing."""
        if image_data is None:
            self.break_signal.emit()  # Notify that processing has finished
            self.is_running = False  # Update running state
            return True  # Return True to indicate that processing should stop
        return False  # Return False if processing should continue


    # TODO: Optimizar las importaciones e inicializaciones, y limpiar un poco el codigo en redundancias.
    # TODO: En la misma idea, considerar transformar FileManager en modulos.

