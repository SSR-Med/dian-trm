from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv
from Api.Controllers.Filters.ExceptionFilter import register_custom_exception_handlers
from Api.Controllers.TrmController import router as trm_router

load_dotenv()  

app = FastAPI(
    title="TRM DIAN API",
    description="Una API para la obtención y almacenamiento de los datos de la DIAN",
    version="1.0.0"
)

register_custom_exception_handlers(app) 

app.include_router(trm_router)

if __name__ == "__main__":
    port = int(os.getenv("PORT")) 
    uvicorn.run(app, host="0.0.0.0", port=port)