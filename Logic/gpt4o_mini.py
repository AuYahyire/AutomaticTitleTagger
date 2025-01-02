import base64
import io
import json

import requests
from PIL import Image
from openai import OpenAI


class ImageAnalyzer:


    def __init__(self, data_manager, env_manager):
        self.client = OpenAI()
        self.data_manager = data_manager
        self.env_manager = env_manager
        self.client.api_key = self.env_manager.get_api_key("OPENAI_API_KEY")

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
            #if not api_key: raise ValueError("API key is not set in the configuration")
            #FIXME Manejar el error de forma diferente

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }

            if not headers["Authorization"]:
                raise ValueError("API key is not set in the configuration")

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "text": system_text,
                                "type": "text"
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
                response_format={
                    "type": "json_schema",
                    "json_schema": {
                        "name": "image_analysis",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "title": {
                                    "type": "string",
                                    "description": "The title of the image analysis."
                                },
                                "keywords": {
                                    "type": "array",
                                    "description": "A list of keywords associated with the image analysis.",
                                    "items": {
                                        "type": "string",
                                        "description": "A keyword related to the image analysis."
                                    }
                                },
                                "category": {
                                    "type": "integer",
                                    "description": "An integer representing the category of the image analysis."
                                }
                            },
                            "required": [
                                "title",
                                "keywords",
                                "category"
                            ],
                            "additionalProperties": False
                        }
                    }
                }
            )
            content = response.choices[0].message.content
            analysis_result = json.loads(content)
            return analysis_result

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

            #AHORA OPENAI RESPONDE EN JSON DIRECTAMENTE, EL FORMATO ES EL ACTUAL, Y HACE FALTA LA INSTANCIA DE OPENAI
            #PARA PODER REALIZAR LLAMADAS A LA API. LO CARGO COMO JSON PARA PODER ACCEDER A EL EN OTRAS AREAS DEL CODIGO.

