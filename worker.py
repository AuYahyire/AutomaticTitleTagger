import os
import csv
import time

from PyQt5.QtCore import QThread, pyqtSignal
import image_processor  # Import processing logic

class ImageProcessorWorker(QThread):
    progress_signal = pyqtSignal(int, str, float, int, int)
    finished_signal = pyqtSignal()

    def __init__(self, image_folder, recursive, config):
        super().__init__()
        self.image_folder = image_folder
        self.recursive = recursive
        self.is_stopped = False
        self.config = config
        self.processImage = image_processor.ImageProcessor(self.config)

    def run(self):
        allowed_extensions = self.config.get('allowed_extensions')

        # Prepare CSV file
        with open('images_titles_and_tags.csv', 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(['Filename', 'Title', 'Keywords', 'Category'])

            # Collect image files
            image_files = []
            if self.recursive:
                for root, _, files in os.walk(self.image_folder):
                    for file in files:
                        if file.split('.')[-1].lower() in allowed_extensions:
                            image_files.append(os.path.join(root, file))
            else:
                image_files = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder)
                               if file.split('.')[-1].lower() in allowed_extensions]

            # Process images
            total_images = len(image_files)
            start_time = time.time()
            for idx, file_path in enumerate(image_files):
                if self.is_stopped:
                    break

                result = self.processImage.process_image(file_path)
                if result:
                    csv_writer.writerow([
                        result['new_filename'],
                        result['title'],
                        result['keywords'],
                        result['category'] if result['category'] is not None else ''
                    ])

                # Calculate elapsed time and estimate remaining time
                elapsed_time = time.time() - start_time
                avg_time_per_image = elapsed_time / (idx + 1)
                remaining_time = avg_time_per_image * (total_images - (idx + 1))

                # Current image to show current/total
                current_image = idx + 1

                # Update progress
                self.progress_signal.emit(int((idx + 1) / total_images * 100), os.path.basename(file_path), remaining_time, current_image, total_images)


        # Emit finished signal
        self.finished_signal.emit()

    def stop(self):
        self.is_stopped = True
