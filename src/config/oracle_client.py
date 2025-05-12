import cx_Oracle # cliente de Oracle en Python
import configparser #Permite pasar las variables de entorno del .ini
import os
import git # Librería para navegar y resolver rutas en repositorios git
import pathlib # Manejar rutas en Python
from pathlib import Path # Crear objetos Path que se puedan manipular para manejar rutas
import argparse # Librería para pasar argumentos por terminal
import logging # Manejar Logging en el scrip
import sys # Añadir al path de python módulos que quieran importar

repo=git.Repo('.', search_parent_directories=True) # '.' Indica que se parte del directorio actual (src/config)... esto ubica la raíz del proyecto en un objeto Repo
repo=pathlib.Path(repo.working_tree_dir) # Se resuelve la ruta como un objeto Path
sys.path.append(str(repo.joinpath("src"))) # Esto es un truco para añadir la ruta al path e importar lo que me venga en gana
print(str(repo)) # debbuging

def get_args():
    """
    Ojo, este método es para definir los argumentos que le debo pasar al script, en 
    este caso el .ini para que lea las variables de entorno para hacer la conexión. 
    """
    parser=argparse.ArgumentParser(description="Cliente de Oracle")
    parser.add_argument("--config_path",
    type=str,
    default="db_config.ini", ## Por simplicidad lo deje en config, si cambia de lógica tienen que resolver la ruta
    help="Ruta al archivo de configuración")

    return parser.parse_args()

def main():
    """
    Ojo! el main es solo para que hagan pruebas locales con el cliente antes de probar los endpoints
    """
    args=get_args()

    logging.basicConfig(level=logging.INFO) #Instancia de Logging... siempre lleven log de la app para hacer el debbuging
    logger=logging.getLogger(__name__)

    logger.info("Cargando configuración del cliente")
    config=load_config_from_ini(args.config_path) # Paso el path del archivo de configuración desde los argumentos
    logger.info("Estableciendo conexión con Oracle")
    client=connect_to_oracle_from_ini(args.config_path)
    logger.info("Conexión a Base de Datos en Oracle Exitosa")



def load_config_from_ini(config_file):

    config=configparser.ConfigParser()
    config.read(config_file) # leo el .ini para leer los párametros de conexión

    return config


def connect_to_oracle_from_ini(config_file):
    config = load_config_from_ini(config_file) # llamo en una instancia el método de carga del ini para leerlo

    username = config["oracle"]["username"] # Leo todos los params de la conexión
    password = config["oracle"]["password"]
    host = config["oracle"]["host"]
    port = config["oracle"]["port"]
    service_name = config["oracle"]["service_name"]

    dsn = f"{host}:{port}/{service_name}" #armo el dns de los parámetros del ini

    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        return connection  

    except cx_Oracle.DatabaseError as e:
        print("Error en la conexión:", e)
        return None  # Esto no es la mejor práctica, deben manejar mejor esta excepción



if __name__ == "__main__":
    main() #Solo para pruebas





