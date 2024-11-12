

direccion_origen = "Calle Costa Rica 49, 18194, Churriana de la Vega, Granada"
csv1 = "data/da_centros.csv"
csv2 = "data/centros_todos.csv"
csv_coincidencias = "data/coincidencias.csv"
csv_centros_exportados= "data/centros_exportados.csv"
csv_bilingues = "data/da_centros_bilingues.csv" 
csv_compensatorios = "data/centros_compensatoria.csv"

# Importa las librerías necesarias
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import csv
from fastapi.responses import FileResponse

app = FastAPI()
# Configuración del middleware CORS (Cross-Origin Resource Sharing)
# Permite que el frontend acceda a la API desde un dominio diferente
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas las origenes. En producción especificar dominios concretos
    allow_credentials=True,  # Permite enviar credenciales en las peticiones
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, etc)
    allow_headers=["*"],  # Permite todas las cabeceras HTTP
)

# Endpoint que devuelve todos los centros educativos en formato JSON
@app.get("/api/centros")
def leer_centros():
    """
    Lee el archivo CSV de centros y lo convierte a formato JSON
    Returns:
        list: Lista de diccionarios con los datos de cada centro
    """
    datos = []
    # Abre el archivo CSV con codificación ISO para caracteres españoles
    with open(csv_centros_exportados, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)  # Crea un lector de CSV que mapea a diccionarios
        # Itera por cada fila y la añade a la lista de datos
        for row in reader:
            datos.append(row)
    return datos

# Endpoint para servir la página principal
@app.get("/", response_class=HTMLResponse)
def get_homepage():
    """
    Sirve el archivo HTML principal de la aplicación
    Returns:
        HTMLResponse: Contenido del archivo index.html
    """
    # Lee el archivo HTML y lo devuelve como respuesta
    with open('frontend/index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()
    return HTMLResponse(content=html_content)

@app.get("/image")
async def get_image():
    """
    Endpoint que sirve una imagen estática
    
    Este endpoint devuelve un archivo de imagen estática ubicado en 'frontend/assets/images/risa.png'
    como FileResponse con tipo de medio image/png.

    Returns:
        FileResponse: Un objeto FileResponse que contiene el archivo de imagen en formato PNG
    """
    return FileResponse("frontend/assets/images/risa.png", media_type="image/png")


