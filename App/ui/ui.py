import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QLabel, QPushButton,
    QCheckBox, QComboBox, QFileDialog, QProgressBar, QHBoxLayout, QSpacerItem, QSizePolicy, QMainWindow,
    QListWidget, QListWidgetItem, QLayout, QApplication, QAction, QStatusBar, QMessageBox, QDialog, QTextEdit
)
from PyQt5.QtGui import QFont, QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, QSize, Qt

from Logic.worker import ImageProcessorWorker


class TituladorApp2(QMainWindow):
    def __init__(self, view_model):
        super().__init__()
        self.view_model = view_model
        self.setWindowIcon(QIcon('../res/icon.png'))
        self.setWindowTitle("Configurador de Titulador")
        self.setGeometry(1450, 800, 1000, 500)

        # Load stylesheet
        self.setStyleSheet(self.load_styles())

        # Main layout setup
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # Left UI layout setup
        self.left_layout = QVBoxLayout()
        self.left_layout.setContentsMargins(10, 10, 10, 10)
        self.left_layout.setSpacing(10)
        self.setup_left_ui_components()
        main_layout.addLayout(self.left_layout)

        # Right layout for file explorer and image viewer
        self.right_layout = QHBoxLayout()
        self.right_layout.setContentsMargins(10, 10, 10, 10)
        self.right_layout.setSpacing(10)
        self.file_view = QListWidget()
        self.file_view.setMinimumSize(400,400)
        self.file_view.setIconSize(QSize(100, 100))
        #self.file_view.setResizeMode(QListWidget.Adjust)
        self.file_view.setUniformItemSizes(True)
        self.file_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.file_view.itemClicked.connect(self.on_file_clicked)  # Conectar la señal para mostrar imágenes
        self.right_layout.addWidget(self.file_view)
        self.auto_load_directory()

        # Image viewer
        self.image_label_layout = QVBoxLayout()
        self.image_label = QLabel('Aquí se mostrarán las imágenes cargadas')
       # self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Filename of Image Viewer
        self.image_label_name = QLabel('')
        self.image_label_name.setAlignment(Qt.AlignCenter)

        self.image_label_layout.addWidget(self.image_label)
        self.image_label_layout.addWidget(self.image_label_name)

        self.right_layout.addLayout(self.image_label_layout)
        main_layout.addLayout(self.right_layout)

        # menu bar
        self.setup_menu_bar()

        # Worker Initialization
        self.worker = None

    def setup_menu_bar(self):
        """Sets up the menu bar."""
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Archivo')
        open_action = QAction('Abrir Configuración', self)
        open_action.triggered.connect(self.open_config)
        file_menu.addAction(open_action)

    def open_config(self):
        """Opens the data_manager.json file and displays its content."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir Configuración", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as f:
                config_data = f.read()
        self.show_config_dialog(file_path, config_data)

    def show_config_dialog(self, file_path, config_data):
        """Displays the data_manager data in a dialog for editing."""
        dialog = QDialog(self)
        dialog.setWindowTitle("Editar Configuración")
        dialog.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit(dialog)
        text_edit.setPlainText(config_data)
        layout.addWidget(text_edit)
        save_button = QPushButton("Guardar", dialog)
        save_button.clicked.connect(lambda: self.save_config(file_path, text_edit.toPlainText()))
        layout.addWidget(save_button)
        dialog.setLayout(layout)
        dialog.exec_()

    def save_config(self, file_path, new_content):
        """Saves the edited data_manager data back to the file."""
        try:
            with open(file_path, 'w', encoding='utf-8') as f: f.write(new_content)
            QMessageBox.information(self, "Éxito", "Configuración guardada correctamente.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al guardar la configuración: {e}")


    def setup_left_ui_components(self):
        """Sets up all UI components in the left layout."""
        self.directory_label = QLabel("Directorio de imágenes:")
        self.directory_input = QLineEdit(self)
        #self.directory_input.setText(self.data_manager.get('last_directory'))
        self.directory_input.setText(self.update_view('last_directory'))

        self.browse_button = QPushButton("Explorar")
        self.browse_button.setFont(QFont('Times', 12))
        self.browse_button.clicked.connect(self.browse_directory)

        # Platform dropdown and recursive checkbox
        self.platform_label = QLabel("Plataforma:")
        self.platform_dropdown = QComboBox(self)
        self.platform_dropdown.addItems(self.update_view('platforms', {}).keys())
        self.platform_dropdown.setCurrentText(self.update_view('last_platform'))

        self.recursive_checkbox = QCheckBox("Recursivo?", self)
        self.recursive_checkbox.setChecked(self.update_view("recursive", False))

        # Progress bar and control buttons
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

        # Progress file info layout
        file_info_layout = QHBoxLayout()
        self.file_label = QLabel('Archivo:')
        self.current_image_label = QLabel('')
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        file_info_layout.addWidget(self.file_label)
        file_info_layout.addSpacerItem(spacer)
        file_info_layout.addWidget(self.current_image_label)

        # Estimated time label
        self.estimated_time_label = QLabel('')

        self.run_button = QPushButton("Ejecutar Titulador")
        self.run_button.clicked.connect(self.run_titulador)
        self.run_button.setFont(QFont('Times', 12))

        self.stop_button = QPushButton("Detener")
        self.stop_button.setFont(QFont('Times', 12))
        self.stop_button.clicked.connect(self.stop_processing)
        self.stop_button.setEnabled(False)

        # status bar
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Falta configurar el API!")

        # Adding widgets and layouts to the left_layout
        widgets_and_layouts = [
            self.directory_label,
            self.directory_input,
            self.browse_button,
            self.platform_label,
            self.platform_dropdown,
            self.recursive_checkbox,
            self.progress_bar,
            file_info_layout,  # Es un layout
            self.estimated_time_label,
            self.run_button,
            self.stop_button,
            self.status_bar
        ]

        for item in widgets_and_layouts:
            if isinstance(item, QLayout):
                self.left_layout.addLayout(item)
            else:
                self.left_layout.addWidget(item)

    def update_view(self, key, default=None):
        return self.view_model.data_manager.get_data(key, default)

    def load_styles(self):
        """Load QSS style settings from file for maintainability."""
        return """
            QWidget { background-color: #2E3440; color: #D8DEE9; font-family: Arial; }
            QLabel { font-size: 16px; }
            QPushButton { background-color: #4C566A; border: 1px solid #D8DEE9; padding: 5px; }
            QPushButton:hover { background-color: #5E81AC; }
            QPushButton:pressed { background-color: #45a049; }
            QLineEdit, QComboBox, QCheckBox { background-color: #3B4252; border: 1px solid #D8DEE9; padding: 5px; }
            QProgressBar::chunk { background-color: #4CAF50; }
        """

    @pyqtSlot()
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Seleccionar Directorio")
        if directory:
            self.directory_input.setText(directory)
            self.update_config()
            self.load_images(directory)
            self.image_label.setText('Haz click en una imágen para mostrarla')
            self.image_label_name.setText('')

    def load_images(self, directory):
        """Clear and load images from the specified directory into file view."""
        self.file_view.clear()
        loading_item = QListWidgetItem("Cargando...")
        self.file_view.addItem(loading_item)
        QApplication.processEvents()  # Actualiza la interfaz de usuario

        for filename in os.listdir(directory):
            if filename.lower().endswith((tuple(self.update_view('allowed_extensions')))):
                file_path = os.path.join(directory, filename)
                item = QListWidgetItem(QIcon(QPixmap(file_path)), filename)
                self.file_view.addItem(item)

        self.file_view.takeItem(self.file_view.row(loading_item))  # Elimina el mensaje de "Cargando..."

    def auto_load_directory(self):
        directory = self.update_view('last_directory')
        if os.path.isdir(directory):
            self.load_images(directory)

    @pyqtSlot(QListWidgetItem)
    def on_file_clicked(self, item):
        """Display the selected image in the image_label."""
        file_path = os.path.join(self.directory_input.text(), item.text())
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                filename = os.path.basename(file_path)
                self.image_label.setFixedSize(400, 400)
                self.image_label.setPixmap(pixmap.scaled(
                    self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
                self.image_label_name.setText(filename)
            else:
                self.image_label.setText('No se pudo cargar la imagen.')

    def update_config(self):
        """Update configuration with current settings and save to file."""
        self.view_model.data_manager.set_data('last_directory', self.directory_input.text())
        self.view_model.data_manager.set_data('recursive', self.recursive_checkbox.isChecked())
        self.view_model.data_manager.set_data('last_platform', self.platform_dropdown.currentText())

    def show_error_message(self, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(message)
        msg.setWindowTitle("Error")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    @pyqtSlot()
    def run_titulador(self):
        """Start image processing."""
        self.disable_ui(True)
        self.update_config()
        image_folder = self.directory_input.text()
        self.worker = ImageProcessorWorker(image_folder, self.recursive_checkbox.isChecked(), self.config)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.on_finished)
        self.worker.start()
        self.stop_button.setEnabled(True)

    @pyqtSlot()
    def stop_processing(self):
        """Stop the processing task."""
        if self.worker:
            self.worker.stop()

    @pyqtSlot(int, str, float, int, int)
    def update_progress(self, value, filename, remaining_time, current_image, total_images):
        self.progress_bar.setValue(value)
        self.file_label.setText(filename)
        self.current_image_label.setText(f"{current_image} / {total_images}")
        self.estimated_time_label.setText(f"Tiempo estimado: {remaining_time:.2f} segundos")

    @pyqtSlot()
    def on_finished(self):
        """Handle processing completion."""
        directory = self.self.update_view('last_directory')
        self.disable_ui(False)
        self.progress_bar.setValue(0)
        self.load_images(directory)
        self.stop_button.setEnabled(False)
        print("Processing complete. Results saved in images_titles_and_tags.csv")

    def disable_ui(self, disable):
        """Enable or disable UI controls for the duration of processing."""
        for widget in [self.directory_input, self.browse_button, self.platform_dropdown, self.recursive_checkbox, self.run_button]:
            widget.setEnabled(not disable)
