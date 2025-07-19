from fastapi import APIRouter, Depends
from Infrastructure.Dtos.QueryResponseDto import QueryResponseDto
from Trm.Application.Dependencies import get_query_handler
from Trm.Application.Queries.GetMonedasQuery import GetMonedasQuery
from Trm.Application.Queries.GetMonedasQueryHandler import GetMonedasQueryHandler
from Trm.Core.Dtos.MonedaDto import MonedaDto

router = APIRouter(
    prefix="/api/trm",
    tags=["TRM"],
    responses={500: {"description": "Internal server error"}}
)

@router.get(
    "/",
    status_code=200,
    response_model=QueryResponseDto[MonedaDto],
    summary="Obtener TRM por fecha",
    description="Obtiene la tasa de cambio del dólar y otras monedas por fecha, filtrando por rango de fechas."
)
async def get_trm(
    query: GetMonedasQuery = Depends(),
    handler: GetMonedasQueryHandler = Depends(get_query_handler)
):
    result = await handler.handle(query)
    return result.model_dump()  