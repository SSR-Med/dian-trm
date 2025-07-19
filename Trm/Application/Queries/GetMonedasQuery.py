from datetime import date
from pydantic import Field
from Infrastructure.Dtos.PaginationDto import PaginationDto

class GetMonedasQuery(PaginationDto):
    fecha_inicio: date = Field(default=date(2024, 1, 1), description="Fecha de inicio")
    fecha_final: date = Field(default=date(2024, 12, 31), description="Fecha final")
