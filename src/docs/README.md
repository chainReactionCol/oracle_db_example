# Oracle DB API - Base de datos del curso

Este proyecto es una aplicación backend construida con **FastAPI** para consumir una base de datos Oracle externa (conectada por VPN). Proporciona una API REST que permite consultar los cursos disponibles en la base de datos.

---

## Estructura del Proyecto

```
oracle_db_example/
                
└── src/
    ├── main.py                     # Punto de entrada principal de la API
    ├── config/
    │   ├── __init__.py
    |   ├── db_config.ini           # Archivo de configuración con credenciales de Oracle
    │   └── oracle_client.py        # Conexión a Oracle a partir de archivo .ini
    └── routers/
        ├── __init__.py
        └── get_courses.py          # Endpoint GET /api/cursos
```

---

## Configuración

### `db_config.ini`

Archivo `.ini` con los parámetros de conexión a Oracle:

```ini
[oracle]
username = TU_USUARIO
password = TU_CONTRASEÑA
host = IP_O_DOMINIO_DEL_SERVIDOR
port = 1521
service_name = LAB
```

Debe estar ubicado config

---

## 🚀 Ejecución del proyecto

### Requisitos

- Python 3.10+
- Oracle Instant Client (preinstalado en la imagen Docker o en el sistema local)
- Base de datos Oracle accesible por VPN

### Ejecutar localmente

Desde la raíz del proyecto:

```bash
python -m uvicorn src.main:app --reload
```

---

## Endpoints disponibles

### GET `/api/cursos`

Retorna todos los cursos registrados en la tabla `COURSE` de la base de datos Oracle.

#### Ejemplo de respuesta:

```json
{
  "cursos": [
    { "id": 1, "nombre": "Historia del Rock", "creditos": 3 },
    { "id": 2, "nombre": "Técnicas de ensayo", "creditos": 2 }
  ]
}
```

---

## Descripción de scripts

### `src/main.py`

- Instancia principal de la aplicación FastAPI.
- Monta los enrutadores.
- Configura el prefijo `/api`.

```python
from fastapi import FastAPI
from src.routers.get_courses import router as courses_router

app = FastAPI(title="API Cursos Oracle")

app.include_router(courses_router, prefix="/api")
```

---

### `src/config/oracle_client.py`

- Carga los parámetros desde `db_config.ini`.
- Establece conexión con Oracle.
- Retorna un objeto `connection` reutilizable.
- También se puede ejecutar como script CLI para probar conexión.

#### Funciones clave:

```python
def load_config_from_ini(config_file: str) -> dict:
    # Lee archivo INI y retorna diccionario de configuración
```

```python
def connect_to_oracle_from_ini(config_file: str) -> cx_Oracle.Connection:
    # Conecta a Oracle y retorna una conexión abierta
```

---

### `src/routers/get_courses.py`

- Define el enrutador para consultar cursos.
- Ejecuta un `SELECT * FROM COURSE`.
- Convierte los resultados a JSON.

#### Endpoint principal:

```python
@router.get("/cursos")
def get_all_courses():
    ...
```

---

## Test de conexión (modo script)

Pueden probar la conexión directamente:

```bash
python src/config/oracle_client.py
```

---

## Posibles mejoras

- Pool de conexiones con `cx_Oracle.SessionPool`
- Manejador de errores global
- Validación de respuestas con `pydantic`
- Autenticación y autorización
- Pruebas unitarias con `pytest`

---

## Autor

- Jorge Luis Sánchez Ruiz
- Referencia para el curso de bases de datos 2025
