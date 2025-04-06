from google.protobuf.json_format import MessageToDict
from google.cloud import vision
from functools import lru_cache
from dotenv import load_dotenv
import os


# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


@lru_cache()
def get_vision_client():
    """
    Creates and caches the Vision API client.

    Returns:
        Vision API client instance
    """
    # Configure Google Cloud Vision API
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_API_KEY_PATH")
    return vision.ImageAnnotatorClient()


# Função para extrair texto de uma imagem usando a API do Google Cloud Vision
def extract_text_from_image(content: bytes) -> dict:
    """
    Extracts text from an image using Google Cloud Vision API.

    Args:
        content: The binary content of the image

    Returns:
        Dictionary containing the extracted text data
    """
    # Get Vision client
    client = get_vision_client()

    # Process image
    image = vision.Image(content=content)
    response = client.text_detection(image=image)

    # Convert response to dictionary
    texts = MessageToDict(response._pb)

    return texts
