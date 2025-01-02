import json
import os

from Data.IFullRepository import IFullRepository


class JsonManager(IFullRepository):
    def __init__(self, file_path, default_json=None):
        self.file_path = file_path
        self.default_json = default_json if default_json is not None else {}
        self.json_data = self.load()

    def load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, ValueError) as e:
                # If the file is empty or contains invalid JSON, create it with default values
                print(f"Error loading JSON: {e}")
                self.save(self.default_json)
                return self.default_json
        else:
            # If the file doesn't exist, create it with default values
            self.save(self.default_json)
        return self.default_json

    def save(self, data=None):
        if data is None:
            data = self.json_data
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    def get(self, key, subkey=None, default=None):
        if subkey:
            return self.json_data.get(key, {}).get(subkey, default)
        else:
            return self.json_data.get(key, default)

    def set(self, key, value, subkey = None, sub_value = None):
        if key == "platforms":
            # Ensure the platforms dictionary exists
            if key not in self.json_data:
                self.json_data[key] = {}

            # If the platform doesn't exist, create it with default texts
            if value not in self.json_data[key]:
                self.json_data[key][value] = {'system_text': "", 'user_text': ""}

            # If update_data is provided, update the existing platform data
            if subkey and sub_value:
                self.json_data[key][value][subkey] = sub_value
        else:
            # For other keys, set the value normally
            self.json_data[key] = value

        self.save()

    def delete(self, key, subkey=None):
        if key in self.json_data:
            if subkey:
                del self.json_data[key][subkey]
            else:
                del self.json_data[key]
        self.save()



DEFAULT_CONFIGURATION = {
    'last_directory': 'ruta/a/tu/archivo',
    'recursive': False,
    'last_platform': '',
    'allowed_extensions': ['jpeg', 'jpg', 'png'],
    'platforms': {
        "LaTostadora": {
            'system_text': "text",
            'user_text': "text2"
        }
    }
}

