from urllib.parse import urlparse
from dotenv import load_dotenv
from logger import info, error
import requests
import hashlib
import time
import jwt
import os


# Load environment variables
load_dotenv()


class BullBankAPI:
    def __init__(self):
        self.base_url = os.getenv("BULLBANK_API_URL")
        self.private_key = open(os.getenv("BULLBANK_PRIVATE_KEY_PATH")).read()
        self.api_key = os.getenv("BULLBANK_API_KEY")

    def _sign_request(self, request_url, request_body=None):
        parsed_url = urlparse(request_url)
        url = parsed_url.path
        if parsed_url.query:
            url += "?" + parsed_url.query

        body = request_body if request_body else "{}"
        body_hash = hashlib.sha256(body.encode("utf-8")).hexdigest()

        now = int(time.time())
        payload = {
            "uri": url,
            "iat": now,
            "exp": now + 55,
            "sub": self.api_key,
            "bodyHash": body_hash,
        }

        headers = {"typ": "JWT", "alg": "RS256"}

        signed_jwt = jwt.encode(
            payload=payload, key=self.private_key, algorithm="RS256", headers=headers
        )

        return f"Bearer {signed_jwt}"

    def obter_transferencias(self):
        url = f"{self.base_url}/transactions"
        auth_token = self._sign_request(url)

        headers = {
            "x-api-key": self.api_key,
            "Authorization": auth_token,
            "Content-Type": "application/json",
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        
        else:
            error(f"Erro ao obter contas: {response.status_code}, {response.text}")
            return None
