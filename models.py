from pydantic import BaseModel


class Solicitud(BaseModel):
    id: int
    estudiante: str
    tipo: str
    estado: str = "en revisión"
