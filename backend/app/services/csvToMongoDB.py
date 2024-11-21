from dotenv import load_dotenv
import os
from pymongo import MongoClient
import csv
import chardet

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
# URI de conexión
client = MongoClient(MONGO_DB_URI)

# Seleccionar base de datos
db = client["CentrosEducativosCluster"]
# Seleccionar colección
collection = db["CentrosAndalucia"]

# Prueba de conexión
print("Conexión exitosa:", db.list_collection_names())


csv_file = os.path.abspath('data/da_centros.csv')
print("Ruta calculada:", csv_file)

# Ruta al archivo CSV
csv_file = 'data/da_centros.csv'


# Intenta cargar los datos del CSV a MongoDB
def detect_encoding(rutaCsv):
    """
    Detecta la codificación de caracteres de un archivo CSV.
    
    Args:
        rutaCsv (str): Ruta al archivo CSV del que se quiere detectar la codificación
        
    Returns:
        str: Codificación detectada del archivo (ej: 'utf-8', 'iso-8859-1', etc.)
    """
    
    # Lee los bytes crudos del archivo sin especificar codificación
    with open(rutaCsv, 'rb') as file:
        raw_data = file.read()
    
    # Utiliza chardet para analizar los bytes y detectar la codificación más probable
    result = chardet.detect(raw_data)
    return result['encoding']


def cargar_MongoDB(rutaCsv):
    """
    Carga datos desde un archivo CSV a MongoDB manejando diferentes codificaciones.

    Args:
        rutaCsv (str): Ruta al archivo CSV que se quiere cargar

    Returns:
        str: Mensaje indicando el resultado de la operación
    """
    # Intenta cargar los datos del CSV a MongoDB
    try:
        # Detectar encoding del archivo usando la función detect_encoding
        encoding = detect_encoding(rutaCsv)
        print(f"Detected encoding: {encoding}")
        
        # Abre el archivo CSV usando el encoding detectado
        with open(rutaCsv, mode='r', encoding=encoding) as file:
            # Para archivos con codificación iso-8859-1 (común en español)
            # usa punto y coma como delimitador
            if encoding == 'iso-8859-1':
                reader = csv.DictReader(file,delimiter=';')
            else:
                # Para otros encodings usa el delimitador por defecto (coma)
                reader = csv.DictReader(file)

            # Itera por cada fila del CSV e inserta en MongoDB
            for row in reader:
                try:
                    # Intenta insertar cada fila como un documento en la colección
                    collection.insert_one(row)
                except Exception as e:
                    # Si hay error en la inserción individual, lo registra y continúa
                    # con el siguiente registro sin detener todo el proceso
                    print(f"Error al insertar registro: {e}")
                    continue

        return "Datos cargados exitosamente."
    
    # Manejo de errores específicos durante el proceso
    except FileNotFoundError:
        return f"Error: No se encontró el archivo {rutaCsv}"
    except PermissionError:
        return "Error: No hay permisos suficientes para leer el archivo"
    except Exception as e:
        return f"Error inesperado: {e}"





