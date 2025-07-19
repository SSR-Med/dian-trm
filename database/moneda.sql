CREATE TABLE moneda (
    id_moneda UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fecha_alta DATE NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_final DATE NOT NULL,
    id_dian INTEGER NOT NULL UNIQUE,
    dolar NUMERIC(19, 5) NOT NULL,
    otras_cotizaciones JSONB NOT NULL
);