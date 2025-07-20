from datetime import date
from pydantic import Field, model_validator
from Infrastructure.Dtos.PaginationDto import PaginationDto
from Infrastructure.Exceptions.BadRequestException import BadRequestException

class GetMonedasQuery(PaginationDto):
    fecha_inicio: date = Field(default=date(2024, 1, 1), description="Fecha de inicio")
    fecha_final: date = Field(default=date(2024, 12, 31), description="Fecha final")

    @model_validator(mode="after")
    def validar_fechas(self):
        hoy = date.today()
        if not (self.fecha_inicio <= self.fecha_final <= hoy and self.fecha_inicio <= hoy):
            raise BadRequestException(
                message="Las fechas proporcionadas no cumplen con las reglas de negocio.",
                detail={
                    "field": "fecha_inicio/fecha_final",
                    "reason": "Las fechas deben estar en orden y no pueden ser mayores a la fecha actual."
                }
            )
        return self