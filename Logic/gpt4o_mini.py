import json
import os
import re
import io
import base64
import requests
from PIL import Image

from Data import enums
from Data.json_manager import JsonManager


class ImageAnalyzer:
    def __init__(self, data_manager, env_manager):
        self.data_manager = data_manager
        self.env_manager = env_manager

    def resize_image(self, image_path, size=(512, 512)):
        with Image.open(image_path) as img:
            img = img.resize(size)
            buffer = io.BytesIO()
            img.save(buffer, format="JPEG")
            buffer.seek(0)
            return buffer

    def encode_image(self, image_buffer):
        return base64.b64encode(image_buffer.read()).decode('utf-8')

    def get_image_analysis(self, parcel):
        try:
            image = parcel['encoded_image']
            system_text = parcel['system_text']
            user_text = parcel['user_text']
            api_key = self.env_manager.get_api_key("OPENAI_API_KEY")
            if not api_key: raise ValueError("API key is not set in the configuration")
            #FIXME Manejar el error de forma diferente

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            if not headers["Authorization"]:
                raise ValueError("API key is not set in the configuration")

            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": system_text
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": user_text
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image}",
                                    "detail": "low"
                                }
                            }
                        ]
                    }
                ],
                "max_tokens": 500,
                "response_format": {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "image_analysis",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {"type": "string"},
                                "keywords": {"type": "array", "items": {"type": "string"}},
                                "category": {"type": "integer"}
                            },
                            "required": ["title", "keywords", "category"],
                            "additionalProperties": False
                        }
                    }
                }
            }

            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            response_json = response.json()
            return json.loads(response_json['choices'][0]['message']['content'])

        except requests.exceptions.RequestException as e:
            print(f"Error making API call, API is not valid: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON response: {e}")
            return None
        except ValueError as e:
            print(f"Configuration error: {e}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None
