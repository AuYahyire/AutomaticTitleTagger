from PyQt5.QtCore import QObject, pyqtSignal

from worker import ImageProcessorWorker


class ImageProcessingSignal(QObject):
    progress_signal = pyqtSignal(int, str, float, int, int)
    finished_signal = pyqtSignal()

    def __init__(self, worker):
        super().__init__()
        self.worker = worker
        self.is_running = False

    def start_processing(self, image_folder, recursive, config):
        """Inicializa y comienza el procesamiento de imágenes."""
        if self.is_running:
            return  # Evita iniciar otro proceso si ya está en ejecución

        self.worker.progress_signal.connect(self.on_progress)
        self.worker.finished_signal.connect(self.on_finished)

        self.is_running = True
        self.worker.start()

    def on_progress(self, progress, filename, remaining_time, current_image, total_images):
        """Actualiza el progreso y reenvía la señal."""
        self.progress_signal.emit(progress, filename, remaining_time, current_image, total_images)

    def on_finished(self):
        """Maneja la finalización del proceso."""
        self.is_running = False
        self.finished_signal.emit()