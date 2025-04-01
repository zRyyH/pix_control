from dotenv import load_dotenv
from logger import info, error
import httpx
import os


# Load environment variables
load_dotenv()


# Classe para interagir com a API do Directus
class DirectusAPI:
    def __init__(self):
        info(f"Iniciando DirectusAPI {os.getenv('DIRECTUS_TOKEN')}")

        self.client = httpx.Client(
            base_url=os.getenv("DIRECTUS_URL_API"),
            headers={"Authorization": f"Bearer {os.getenv('DIRECTUS_TOKEN')}"},
            timeout=30,
        )

    def post_directus(self, endpoint, json=None, files=None, params=None):
        try:
            response = self.client.post(
                endpoint,
                json=json,
                files=files,
                params=params,
            )

            response.raise_for_status()

            info(f"Requisição POST ao directus, endpoint: {endpoint}")

            return response.json()

        except httpx.RequestError as e:
            error(
                f"Erro ao fazer requisição ao directus, endpoint: {endpoint}, json: {json}, files: {files}, params: {params}, erro: {e}"
            )
            raise Exception(f"Erro ao fazer requisição POST ao directus")

    def get_directus(self, endpoint, params=None):
        try:
            info(f"Requisição GET ao directus, endpoint: {endpoint}, params: {params}")

            response = self.client.get(endpoint, params=params)
            response.raise_for_status()

            return response.json()

        except httpx.RequestError as e:
            error(
                f"Erro ao fazer requisição ao directus, endpoint: {endpoint}, params: {params}, erro: {e}"
            )
            raise Exception(f"Erro ao fazer requisição GET ao directus")
