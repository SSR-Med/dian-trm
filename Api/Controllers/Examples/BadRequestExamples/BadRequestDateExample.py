from pydantic import BaseModel, Field
from typing import Optional

class BadRequestDateExample(BaseModel):
    message: str = Field(..., description="Un mensaje general describiendo el error.")
    detail: Optional[dict] = Field(None, description="Detalles adicionales sobre el error, si están disponibles.")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "message": "Las fechas proporcionadas no cumplen con las reglas de negocio.",
                    "detail": {
                        "field": "fecha_inicio/fecha_final",
                        "reason": "Las fechas deben estar en orden y no pueden ser mayores a la fecha actual."
                    }
                }
            ]
        }
    }