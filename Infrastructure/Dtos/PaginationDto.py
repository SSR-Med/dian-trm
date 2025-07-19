from pydantic import BaseModel, Field

class PaginationDto(BaseModel):
    page: int = Field(1, gt=0, description="Número de página")
    page_size: int = Field(10, gt=0, description="Tamaño de página")
