from typing import Dict, Generic, TypeVar, List, Any
from pydantic import BaseModel

T = TypeVar('T')

class QueryResponseDto(BaseModel, Generic[T]):
    page: int
    page_size: int
    has_next: bool
    has_previous: bool
    results: List[T]
    total_count: int
   
    @classmethod
    def success(
        cls,
        page: int,
        page_size: int,
        has_next: bool,
        has_previous: bool,
        results: List[T],
        total_count: int
    ) -> 'QueryResponseDto[T]':
        return cls(
            page=page,
            page_size=page_size,
            has_next=has_next,
            has_previous=has_previous,
            results=results,
            total_count=total_count
        )
   
    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump() 