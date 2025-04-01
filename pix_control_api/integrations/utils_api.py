from dotenv import load_dotenv
import requests
import jwt
import os


# Load environment variables
load_dotenv()


class UtilsAPI:
    def __init__(self):
        # URL base do SDK
        self.url_base = os.getenv("UTILS_URL_API")

        # Token JWT para autenticação
        token = jwt.encode({}, os.getenv("UTILS_SECRET_KEY_API"), algorithm="HS256")

        # Headers para requisições
        self.headers = {"Authorization": f"Bearer {token}"}

    def _post_utils(self, endpoint, json=None, files=None, params=None):
        res = requests.post(
            url=self.url_base + endpoint,
            headers=self.headers,
            json=json,
            files=files,
            params=params,
        )

        # Verifica se a requisição foi bem-sucedida
        res.raise_for_status()

        # Retorna o JSON da resposta
        return res.json()

    def _get_utils(self, endpoint, params=None):
        res = requests.get(
            url=self.url_base + endpoint,
            headers=self.headers,
            params=params,
        )

        # Verifica se a requisição foi bem-sucedida
        res.raise_for_status()

        # Retorna o JSON da resposta
        return res.json()

    # Extrair dados importantes de uma mensagem
    def extract_important_data(self, message):
        return self._post_utils(
            endpoint="/api/extract-important-data",
            json={"message": message},
        )

    # Extrair texto de um arquivo xlsx
    def extract_text_from_xlsx(self, file, sheet=0, start_row=1, end_row=None):
        return self._post_utils(
            endpoint="/api/extract-text-from-xlsx",
            files={"file": file},
            params={
                "sheet_index": sheet,
                "start_row": start_row,
                "end_row": end_row,
            },
        )

    # Extrair texto de um arquivo pdf
    def extract_text_from_pdf(self, file):
        return self._post_utils(
            endpoint="/api/extract-text-from-pdf",
            files={"file": file},
        )

    # Extrair texto de uma imagem
    def extract_text_from_image(self, file):
        return self._post_utils(
            endpoint="/api/extract-text-from-image",
            files={"file": file},
        )
