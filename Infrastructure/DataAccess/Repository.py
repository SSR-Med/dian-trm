from typing import Generic, TypeVar, Type, List, Optional, Callable, Tuple, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc, select, func
from sqlalchemy.sql import Select

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db = db_session
        self.model = model

    async def get_all(
        self,
        pagination: Tuple[int, int] = (1, 10),
        filter_func: Optional[Callable[[Type[T]], Any]] = None,
        order_by: Optional[str] = None,
        order_direction: str = "asc"
    ) -> Dict[str, Any]:
        page, page_size = pagination
        
        data_query: Select = select(self.model)
        if filter_func:
            data_query = data_query.where(filter_func(self.model))
        
        if order_by:
            if hasattr(self.model, order_by):
                field = getattr(self.model, order_by)
                if order_direction.lower() == "desc":
                    data_query = data_query.order_by(desc(field))
                else:
                    data_query = data_query.order_by(asc(field))
            else:
                raise AttributeError(f"El modelo {self.model.__name__} no tiene el atributo '{order_by}'")
        
        count_query: Select = select(func.count()).select_from(self.model)
        if filter_func:
            count_query = count_query.where(filter_func(self.model))
        
        total_count = (await self.db.execute(count_query)).scalar_one()
        
        offset = (page - 1) * page_size
        data_query = data_query.offset(offset).limit(page_size)
        
        result = await self.db.execute(data_query)
        data = result.scalars().all()
        
        has_next = (page * page_size) < total_count
        has_previous = page > 1
        
        return {
            "data": data,
            "has_next": has_next,
            "has_previous": has_previous,
            "total_count": total_count,
        }

    async def add(self, entity: T) -> None:
        self.db.add(entity)

    async def add_many(self, entities: List[T]) -> None:
        self.db.add_all(entities)

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()