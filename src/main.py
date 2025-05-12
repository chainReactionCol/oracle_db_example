# Este es el enrutador, recibe todas las rutas de la app 
from fastapi import FastAPI
from src.routers.get_courses import router as courses_router

app = FastAPI(title="API Universidad Curso BDD 2025-I Oracle")

app.include_router(courses_router, prefix="/api") # Incluyo la ruta y el prefijo con el que se va a invocar


