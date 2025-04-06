from dotenv import load_dotenv
from logger import info, error, warning
import httpx
import json
import os


# Load environment variables
load_dotenv()


# Classe para interagir com a API do Directus
class DirectusAPI:
    def __init__(self):
        self.client = httpx.Client(
            base_url=os.getenv("DIRECTUS_URL_API"),
            headers={"Authorization": f"Bearer {os.getenv('DIRECTUS_TOKEN')}"},
            timeout=30,
        )

    def patch_directus(self, endpoint, json_data=None, params=None):
        try:
            response = self.client.patch(
                endpoint,
                json=json_data,
                params=params,
            )

            if "errors" in response.json().keys():
                log = json.dumps(response.json(), indent=4)
                raise Exception(f"Erro: {log}")

            return response.json()

        except httpx.RequestError as e:
            raise Exception(e)

    def post_directus(self, endpoint, json_data=None, files=None, params=None):
        try:
            response = self.client.post(
                endpoint,
                json=json_data,
                files=files,
                params=params,
            )

            if "errors" in response.json().keys():
                log = json.dumps(response.json(), indent=4)
                raise Exception(f"Erro: {log}")

            return response.json()

        except httpx.RequestError as e:
            raise Exception(e)

    def get_directus(self, endpoint, params=None):
        try:
            response = self.client.get(endpoint, params=params)

            if "errors" in response.json().keys():
                log = json.dumps(response.json(), indent=4)
                raise Exception(f"Erro: {log}")

            return response.json()

        except httpx.RequestError as e:
            raise Exception(e)
