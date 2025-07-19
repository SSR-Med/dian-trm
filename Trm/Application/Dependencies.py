from Infrastructure.DataAccess.Configurations.DatabaseConfig import get_db
from Infrastructure.DataAccess.UnitOfWork import UnitOfWork
from Infrastructure.Services.DianService import DianService
from Trm.Application.Queries.Mappers.MonedaMapper import MonedaMapper
from Trm.Application.Queries.GetMonedasQueryHandler import GetMonedasQueryHandler
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

def get_query_handler(db: AsyncSession = Depends(get_db)):
    uow = UnitOfWork(lambda: db)
    dian_service = DianService()
    moneda_mapper = MonedaMapper()
    return GetMonedasQueryHandler(uow, dian_service, moneda_mapper)