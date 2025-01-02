from PyQt5.QtCore import QObject, pyqtSignal

from Logic.gpt4o_mini import ImageAnalyzer
from Logic.image_processor import ImageProcessor
from Logic.worker.worker import ImageProcessorWorker


class LogicViewModel(QObject):
    progress_signal = pyqtSignal(dict)  # Change to emit a dictionary

    def __init__(self, data_manager, env_manager):
        super().__init__()
        self.data_manager = data_manager
        self.env_manager = env_manager
        self.analyzer = None
        self.processor = None
        self.worker = None
        self._progress = 0
        self._filename = ""
        self._remaining_time = 0.0
        self._current_image = 0
        self._total_images = 0

    def initialize_execution(self):
        image_folder = self.data_manager.get_data('last_directory')
        recursive = self.data_manager.get_data('recursive')
        allowed_extensions = self.data_manager.get_data('allowed_extensions')
        platform = self.data_manager.get_data('last_platform')
        platform_data = self.data_manager.get_data('platforms').get(platform, {})
        system_text = platform_data.get('system_text')
        user_text = platform_data.get('user_text')

        self.analyzer = ImageAnalyzer(self.data_manager, self.env_manager)
        self.processor = ImageProcessor(self.data_manager, self.analyzer)
        self.worker = ImageProcessorWorker(image_folder, recursive, self.processor, allowed_extensions, user_text,
                                           system_text)

        # Connect the progress signal to the updated method
        self.processor.progress_signal.connect(self.update_progress)
        self.worker.break_signal.connect(self.execution_break)
        self.worker.finished_signal.connect(self.execution_finished)

        # Start the worker thread
        self.worker.start()

    def update_progress(self, progress_data):
        """Update the view model with progress data from the worker."""
        self._progress = progress_data['progress_percentage']
        self._filename = progress_data['current_file']
        self._remaining_time = progress_data['remaining_time']
        self._current_image = progress_data['current_image_number']
        self._total_images = progress_data['total_images']

        # Emit the progress signal, if needed, for the UI updates
        self.progress_signal.emit(progress_data)

    def execution_finished(self):
        print("Worker off")

    def execution_break(self):
        pass
    # TODO: Implement the logic for stopping the execution
    def stop_execution(self):
        if self.worker:
            self.worker.stop()
            self.worker.wait()  # Wait for the worker to finish
            self.worker = None  # Reset the worker
            self.analyzer = None
            self.processor = None
            self._progress = 0
            self._filename = ""
            self._remaining_time = 0.0
            self._current_image = 0
            self._total_images = 0
