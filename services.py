import random
from models import Solicitud


def validar_token(token: str) -> bool:
    return token is not None and token.startswith("Bearer ")


def enviar_a_certificacion(solicitud: Solicitud) -> str:
    return random.choice(["procesado", "en revisión", "rechazado"])
