from fastapi import APIRouter #Los routers
import pathlib
from pathlib import Path
from src.config.oracle_client import connect_to_oracle_from_ini # Súper importante!!! traigo el método de conexión aislando funcionamiento

router = APIRouter() #instancia del router

@router.get("/cursos") #endpoint get (en el crud me permite leer datos)
def get_all_courses():
    try:
        
        config_path = Path(__file__).resolve().parents[1] / "config" / "db_config.ini" #paso el path del archivo de configuración, hago la conexión y creo un cursor
        print(str(config_path))
        connection = connect_to_oracle_from_ini(str(config_path))
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM COURSE") # Acá está la magia y el SQL.... :) La query invocada a la base de datos.

        columnas = [col[0].lower() for col in cursor.description] # Uso una comprensión de listas para hacer una lista con las tuplas retornadas trayendo los nombres de estas
        resultados = [dict(zip(columnas, row)) for row in cursor.fetchall()] # Otra comprensión de listas para armar un diccionario con claves los nombres de las columnas y valores los datos

        return {"cursos": resultados} #devuelvo el diccionario

    except Exception as e:
        return {"error": str(e)}

    finally:
        try:
            cursor.close()
            connection.close() # Cierro la conexión
        except:
            pass


    