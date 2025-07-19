from Trm.Core.Entities.Moneda import Moneda
from Infrastructure.Dtos.TRMDto import TRMDto

class MonedaMapper:
    def __init__(self) -> None:
        pass

    def trm_dto_to_entity(self, trm_dto: TRMDto) -> Moneda:
        return Moneda(
            fecha_alta=trm_dto.fecha_alta,
            fecha_inicio=trm_dto.fecha_inicio,
            fecha_final=trm_dto.fecha_final,
            id_dian=trm_dto.id_dian,
            dolar=trm_dto.dolar,
            otras_cotizaciones=trm_dto.otras_cotizaciones
        )