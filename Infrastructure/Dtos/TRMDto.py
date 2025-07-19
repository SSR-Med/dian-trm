from pydantic import BaseModel
from datetime import date

class TRMDto(BaseModel):
    fecha_alta: date
    fecha_inicio: date
    fecha_final: date
    id_dian: int
    dolar: float
    dolar_hong_kong: float
    reminbi: float