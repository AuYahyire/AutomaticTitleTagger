import os
import time
from PyQt5.QtCore import pyqtSignal, QObject
from Logic.file_manager import FileManager


class ImageProcessor(QObject):
    progress_signal = pyqtSignal(dict)

    def __init__(self, data_manager, analyzer):
        super().__init__()
        self.data_manager = data_manager
        self.analyzer = analyzer
        self.total_processed_images = 0

    def process_image(self, all_image_files_path, system_text, user_text, total_images):
        image_data = []
        start_time = time.time()  # Marca el tiempo de inicio

        try:
            for file in all_image_files_path:
                # Primero, incrementamos el índice
                self.update_progress(total_images, start_time, file)

                # Luego procesamos el archivo
                parcel = FileManager.create_parcel(file, system_text, user_text)
                if parcel is None:
                    print(f"Error: parcel is None for file {file}")
                    break  # Si no se puede crear el parcel, salimos del bucle

                # Analizar la imagen
                analysis = self.analyzer.get_image_analysis(parcel)
                if analysis is None:
                    print(f"Error: the API call is returning None for file {file}")
                    return None  # Abortamos si la API no devuelve un análisis

                # Sanitizar el nombre del archivo
                sanitized_filename = FileManager.sanitize_filename(analysis['title'])
                file_extension = FileManager.get_file_extension(file)
                new_filename = sanitized_filename + file_extension

                # Construir la nueva ruta del archivo
                new_file_path = os.path.join(os.path.dirname(file), new_filename)

                # Asegurarse de que el nuevo archivo no exista, si existe agregar contador
                counter = 1
                while FileManager.file_exists(new_file_path):
                    new_filename = f"{sanitized_filename}_{counter}{file_extension}"
                    new_file_path = os.path.join(os.path.dirname(file), new_filename)
                    counter += 1

                # Renombrar el archivo
                os.rename(file, new_file_path)

                # Actualizar los metadatos de la imagen
                FileManager.update_image_metadata(new_file_path, analysis['title'], analysis['keywords'],
                                                  analysis['category'])

                # Agregar los datos de la imagen procesada
                image_data.append({
                    'original_filename': os.path.basename(file),
                    'new_filename': new_filename,
                    'title': analysis['title'],
                    'keywords': ', '.join(analysis['keywords']),
                    'category': analysis['category'] if self.data_manager.get_data(
                        'last_platform') == "Adobe Stock" else None
                })

                # Aumentar el índice después de procesar el archivo
                self.total_processed_images += 1


        except Exception as e:
            print(f"Error processing images: {e}")
            return None

        return image_data  # Retornar los datos de imagen procesados

    def update_progress(self, total_images, start_time, file_path):
        """Update the progress signal and calculate remaining time."""
        elapsed_time = time.time() - start_time  # Tiempo transcurrido
        avg_time_per_image = elapsed_time / (self.total_processed_images + 1) if self.total_processed_images > 0 else 0  # Evita división por cero
        remaining_time = avg_time_per_image * (total_images - (self.total_processed_images + 1))  # Tiempo restante estimado


        # Prepare progress data as a dictionary
        progress_data = {
            'progress_percentage': int((self.total_processed_images + 1) / total_images * 100),  # Porcentaje de progreso
            'current_file': os.path.basename(file_path),  # Nombre del archivo actual
            'remaining_time': remaining_time,  # Tiempo restante
            'current_image_number': self.total_processed_images,  # Número de imagen actual
            'total_images': total_images  # Total de imágenes
        }

        # Emit progress signal with the prepared data
        self.progress_signal.emit(progress_data)

                # Print progress data for debugging
        print(f"Progress: {progress_data['progress_percentage']}%, "
              f"Current File: {progress_data['current_file']}, "
              f"Remaining Time: {progress_data['remaining_time']} seconds, "
              f"Current Image Number: {progress_data['current_image_number']}, "
              f"Total Images: {progress_data['total_images']}")

    # TODO: Handle the case when progress is interrupt, so to not lose progress if reanuding, also informing user if wants to resume or restart.