import piexif

class MetadataManager:
    @staticmethod
    def update_image_metadata(image_path, title, keywords, category):
        if image_path.lower().endswith(('.jpg', '.jpeg')):
            exif_dict = piexif.load(image_path)
            exif_dict['0th'][piexif.ImageIFD.ImageDescription] = title.encode('utf-8')
            exif_dict['0th'][piexif.ImageIFD.XPKeywords] = ', '.join(keywords).encode('utf-16le')
            exif_dict['0th'][piexif.ImageIFD.XPSubject] = str(category).encode('utf-16le')
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, image_path)

    # TODO: Consider adding some footprints for statistic or logic.