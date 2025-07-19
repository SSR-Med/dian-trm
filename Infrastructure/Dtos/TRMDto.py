from pydantic import BaseModel
from datetime import date
from typing import Dict, Any

class TRMDto(BaseModel):
    fecha_alta: date
    fecha_inicio: date
    fecha_final: date
    id_dian: int
    dolar: float
    otras_cotizaciones: Dict[str, Any] 