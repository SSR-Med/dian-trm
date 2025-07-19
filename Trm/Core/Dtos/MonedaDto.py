from pydantic import BaseModel
from decimal import Decimal
from datetime import date
from uuid import UUID
from typing import Dict, Any 

class MonedaDto(BaseModel):
    id_moneda: UUID
    fecha_alta: date
    fecha_inicio: date
    fecha_final: date
    id_dian: int
    dolar: Decimal
    otras_cotizaciones: Dict[str, Any] 

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_object(cls, moneda_orm) -> 'MonedaDto':
        return cls(
            id_moneda=moneda_orm.id_moneda,
            fecha_alta=moneda_orm.fecha_alta,
            fecha_inicio=moneda_orm.fecha_inicio,
            fecha_final=moneda_orm.fecha_final,
            id_dian=moneda_orm.id_dian,
            dolar=moneda_orm.dolar,
            otras_cotizaciones=moneda_orm.otras_cotizaciones 
        )