# 📈 Currency Quotes Scraper DIAN

Proyecto en **FastAPI** que permite obtener las cotizaciones del dólar y otras monedas desde el sitio oficial de la **DIAN** de Colombia, según un rango de fechas definido. Implementa una arquitectura limpia basada en **Hexagonal (Ports & Adapters)**, **CQRS**, y uso de **caché** para mejorar el rendimiento en consultas recurrentes.

---

## 📋 Tabla de Contenido

- [🧠 Características Principales](#-características-principales)
- [🧱 Arquitectura](#-arquitectura)
- [⚙️ Tecnologías](#️-tecnologías)
- [🚀 Instalación](#-instalación)
- [👨‍💻 Créditos y Licencia](#-créditos-y-licencia)

---

## 🧠 Características Principales

- Consulta automatizada de cotizaciones en la página de la DIAN.
- Filtros por fecha de inicio y fecha final.
- Paginación en las consultas.
- Arquitectura limpia (Hexagonal).
- Separación clara entre comandos y queries (CQRS).
- Uso de caché para optimizar acceso a datos ya consultados.
- Persistencia de resultados en PostgreSQL bajo demanda.

---

## 🧱 Arquitectura

Este proyecto sigue los principios de la **Arquitectura Hexagonal** o **Ports & Adapters**, con separación de responsabilidades en capas:

- **Domain**: lógica de negocio y modelos principales.
- **Application**: comandos (escritura), queries (lectura) y casos de uso.
- **Infrastructure**: servicios externos (web scraping DIAN, base de datos, caché).
- **API**: entrada HTTP mediante FastAPI.

> También se implementa CQRS (Command Query Responsibility Segregation), dividiendo las operaciones de lectura y escritura en rutas y handlers independientes.

---

## ⚙️ Tecnologías

- **FastAPI** (API REST)
- **PostgreSQL** (almacenamiento persistente)
- **Requests / BeautifulSoup4** (web scraping desde DIAN)
- **Pydantic** (validación y serialización de datos)
- **Uvicorn** (servidor ASGI)

---

## 🚀 Instalación

```bash
# Clonar el repositorio
git clone https://github.com/SSR-Med/dian-trm

# Instalar dependencias
pip install -r requirements.txt

# Crear archivo .env (basado en .env.example)
cp .env.example .env

# Iniciar el servidor
python3 main.py
```

# 👨‍💻 Créditos del Proyecto

Este proyecto fue desarrollado con fines educativos y de uso libre. Si decides reutilizarlo o modificarlo, por favor reconoce el trabajo de sus autores originales.

## Autores

- **Juan Camilo Ospina Palma**
- **Santiago Salazar Ramírez**

---

Este software es de código abierto y está disponible bajo licencia MIT. Eres libre de utilizarlo y adaptarlo a tus necesidades, siempre que cites la fuente correspondiente.
