import os
import re

import piexif

from gpt4o_mini import ImageAnalyzer


class ImageProcessor:
    def __init__(self, config):
        self.config = config
        self.analyzer = ImageAnalyzer(config)

    def sanitize_filename(self, filename):
        return re.sub(r'[^\w\s-]', '', filename).strip().replace(' ', '_')

    def update_image_metadata(self, image_path, title, keywords, category):
        if image_path.lower().endswith(('.jpg', '.jpeg')):
            exif_dict = piexif.load(image_path)
            exif_dict['0th'][piexif.ImageIFD.ImageDescription] = title.encode('utf-8')
            exif_dict['0th'][piexif.ImageIFD.XPKeywords] = ', '.join(keywords).encode('utf-16le')
            exif_dict['0th'][piexif.ImageIFD.XPSubject] = str(category).encode('utf-16le')
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, image_path)

    def process_image(self, file_path):
        try:
            analysis = self.analyzer.get_image_analysis(file_path)
            new_filename = self.sanitize_filename(analysis['title']) + os.path.splitext(file_path)[1]
            new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
            counter = 1
            while os.path.exists(new_file_path):
                new_filename = f"{self.sanitize_filename(analysis['title'])}_{counter}{os.path.splitext(file_path)[1]}"
                new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
                counter += 1

            os.rename(file_path, new_file_path)
            self.update_image_metadata(new_file_path, analysis['title'], analysis['keywords'], analysis['category'])

            return {
                'original_filename': os.path.basename(file_path),
                'new_filename': new_filename,
                'title': analysis['title'],
                'keywords': ', '.join(analysis['keywords']),
                'category': analysis['category'] if self.config.get('last_platform') == "Adobe Stock" else None
            }

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            return None