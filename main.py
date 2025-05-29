from fastapi import FastAPI, Depends, Request, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models import Solicitud
from services import enviar_a_certificacion
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Middleware CORS (por si luego consumes desde otros orígenes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seguridad básica tipo Bearer Token
bearer_scheme = HTTPBearer()

solicitudes_db = {}


def validar_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    if not token:
        raise HTTPException(status_code=401, detail="Token inválido")
    return token


@app.post("/solicitudes")
async def crear_solicitud(solicitud: Solicitud, token: str = Depends(validar_token)):
    estado = enviar_a_certificacion(solicitud)
    solicitud.estado = estado
    solicitudes_db[solicitud.id] = solicitud
    return {"mensaje": "Solicitud procesada", "estado": estado}


@app.get("/solicitudes/{id}")
async def obtener_solicitud(id: int, token: str = Depends(validar_token)):
    solicitud = solicitudes_db.get(id)
    if not solicitud:
        raise HTTPException(status_code=404, detail="No encontrada")
    return solicitud
