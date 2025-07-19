from sqlalchemy import Column, Date, Integer, Numeric, func
from sqlalchemy.dialects.postgresql import UUID, JSONB # Importamos JSONB
from Infrastructure.DataAccess.Configurations.DatabaseConfig import Base

class Moneda(Base):
    __tablename__ = "moneda"

    id_moneda = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        server_default=func.gen_random_uuid()
    )
    fecha_alta = Column(Date, nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_final = Column(Date, nullable=False)
    id_dian = Column(Integer, nullable=False, unique=True)
    dolar = Column(Numeric(19, 5), nullable=False)
    otras_cotizaciones = Column(JSONB, nullable=False) 