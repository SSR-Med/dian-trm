from datetime import timedelta, date
from Infrastructure.DataAccess.Repository import Repository
from Infrastructure.DataAccess.UnitOfWork import UnitOfWork
from Infrastructure.Dtos.QueryResponseDto import QueryResponseDto
from Infrastructure.Services.DianService import DianService
from Trm.Application.Queries import GetMonedasQuery
from Trm.Application.Queries.Mappers.MonedaMapper import MonedaMapper
from Trm.Core.Dtos.MonedaDto import MonedaDto
from Trm.Core.Entities.Moneda import Moneda
import sys

class GetMonedasQueryHandler:
    def __init__(self, uow: UnitOfWork, dian_service: DianService, moneda_mapper: MonedaMapper) -> None:
        self.uow = uow
        self.dian_service = dian_service
        self.moneda_mapper = moneda_mapper
        
    def _get_all_fridays_in_range(self, start_date: date, end_date: date) -> set[date]:
        if start_date > end_date:
            return set()
        
        days_until_first_friday = (4 - start_date.weekday() + 7) % 7
        first_friday = start_date + timedelta(days=days_until_first_friday)
        
        if first_friday > end_date:
            return set()
        
        fridays = {
            first_friday + timedelta(weeks=n)
            for n in range(int((end_date - first_friday).days / 7) + 1)
            if (first_friday + timedelta(weeks=n)) <= end_date
        }
        return fridays
   
    async def handle(self, query: GetMonedasQuery) -> QueryResponseDto[MonedaDto]:
        async with self.uow as session:
            try:
                repo = await self.uow.get_repository_with_session(session, Moneda)
                
                filter_func = lambda M: (M.fecha_alta >= query.fecha_inicio) & \
                                        (M.fecha_alta <= query.fecha_final)
                
                repo_result = await repo.get_all(
                    pagination=(query.page, sys.maxsize),
                    filter_func=filter_func
                )
                
                fechas_alta_database = {moneda.fecha_alta for moneda in repo_result["data"]}
                fechas_viernes = self._get_all_fridays_in_range(query.fecha_inicio, query.fecha_final)

                fechas_interseccion = fechas_viernes.difference(fechas_alta_database)
                
                if fechas_interseccion:
                    trm_dtos = [await self.dian_service.obtener_datos_trm(fecha) for fecha in fechas_interseccion]
                    monedas = [self.moneda_mapper.trm_dto_to_entity(trm_dto) for trm_dto in trm_dtos]
                    await self.save_monedas(repo, monedas) 
                    await repo.commit()
                
                repo_result = await repo.get_all(
                    pagination=(query.page, query.page_size),
                    filter_func=filter_func,
                    order_by="id_dian",
                    order_direction="desc"
                )
                
                monedas_dto = [MonedaDto.from_orm_object(moneda) for moneda in repo_result["data"]]
                
                return QueryResponseDto.success(
                    page=query.page,
                    page_size=query.page_size,
                    has_next=repo_result["has_next"],
                    has_previous=repo_result["has_previous"],
                    results=monedas_dto,
                    total_count=repo_result["total_count"],
                )
            except Exception as e:
                raise
            
    async def save_monedas(self, repo: 'Repository', monedas: list[Moneda]) -> None:
        await repo.add_many(monedas)