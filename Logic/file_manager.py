import csv
import os
import re
import io
import base64
from tracemalloc import Statistic

import piexif
from PIL import Image

class FileManager:
    @staticmethod
    def sanitize_filename(filename):
        return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)

    @staticmethod
    def rename_file(old_path, new_path):
        os.rename(old_path, new_path)

    @staticmethod
    def get_file_extension(file):
        return os.path.splitext(file)[1]

    @staticmethod
    def filter_image_files(files, allowed_extensions):
        return [file for file in files if file.split('.')[-1].lower() in allowed_extensions]

    @staticmethod
    def create_csv(root, folder_name, image_data):
        """
        Crea un archivo CSV en la ruta especificada con los datos de las imágenes.

        :param folder_name:
        :param root: Ruta del directorio donde se creará el CSV
        :param image_data: Lista de diccionarios con los datos de las imágenes
        """
        csv_path = os.path.join(root, f"{folder_name}.csv")
        with open(csv_path, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file)
            # Escribir encabezados
            csv_writer.writerow(['Filename', 'Title', 'Keywords', 'Category'])
            # Escribir datos de cada imagen
            for data in image_data:
                csv_writer.writerow([data['new_filename'], data['title'], data['keywords'], data['category']])

    @staticmethod
    def create_parcel(file_path, system_text, user_text):
        resized = FileManager.resize_image(file_path)
        encoded = FileManager.encode_image(resized)
        parcel = {
            'encoded_image': encoded,
            'system_text': system_text,
            'user_text': user_text
        }
        return parcel

    @staticmethod
    def resize_image(image_path, size=(512, 512)):
        with Image.open(image_path) as img:
            img = img.resize(size)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)
            return buffer

    @staticmethod
    def encode_image(image_buffer):
        return base64.b64encode(image_buffer.read()).decode('utf-8')

    @staticmethod
    def update_image_metadata(image_path, title, keywords, category):
        if image_path.lower().endswith(('.jpg', '.jpeg')):
            exif_dict = piexif.load(image_path)
            exif_dict['0th'][piexif.ImageIFD.ImageDescription] = title.encode('utf-8')
            exif_dict['0th'][piexif.ImageIFD.XPKeywords] = ', '.join(keywords).encode('utf-16le')
            exif_dict['0th'][piexif.ImageIFD.XPSubject] = str(category).encode('utf-16le')
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, image_path)
