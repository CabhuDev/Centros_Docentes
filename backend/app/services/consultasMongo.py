from pymongo import MongoClient
import os
from dotenv import load_dotenv
from backend.app.utils.regex import *

# Cargar las variables de entorno
load_dotenv()

MONGO_DB_URI = os.getenv("MONGO_DB_URI")
client = MongoClient(MONGO_DB_URI)

# Conexión a la base de datos y colección
db = client["CentrosEducativosCluster"]
collection = db["CentrosAndalucia"]



def obtener_centros_filtrados(localidad=None, 
                                etapa=None, 
                                provincia=None,
                                codigo=None,
                                nombreCentro=None,
                                tipoCentro=None):
    """
    Obtiene una lista de centros filtrados según los parámetros proporcionados.
    Args:
        localidad (str, optional): Localidad del centro.
        etapa (str, optional): Etapa educativa del centro.
        provincia (str, optional): Provincia del centro.
        codigo (str, optional): Código del centro.
        nombreCentro (str, optional): Nombre específico del centro.
        tipoCentro (str, optional): Tipo de centro.
    Returns:
        list: Lista de centros que coinciden con los filtros proporcionados.
    """
    try:
        # Crear un diccionario de consulta vacío
        query = {}
        
        # Agregar filtros a la consulta si se proporcionan
        if localidad:
            query["D_LOCALIDAD"] = {"$regex": patron_coincidencia_exacta(localidad)}
        if etapa:
            query[etapa] = "Sí"
        if provincia:
            query["D_PROVINCIA"] = {"$regex": patron_coincidencia_exacta(provincia)}
        if codigo:
            query["codigo"] = {"$regex": patron_coincidencia_exacta(codigo)}
        if nombreCentro:
            query["D_ESPECIFICA"] = {"$regex": patron_coincidencia_parcial(nombreCentro)}
        if tipoCentro:
            query["D_DENOMINA"] = tipoCentro

        # Imprimir el tipo de centro recibido y la consulta generada para depuración
        print(f"Tipo de centro recibido: {tipoCentro}")
        print(f"Consulta generada: {query}")
        
        # Ejecutar la consulta en la colección y devolver los resultados como una lista
        return list(collection.find(query, {"_id": 0}))
    
    
    except Exception as e:
        print(f"Error al obtener centros filtrados: {str(e)}")
        return []  # Retorna lista vacía en caso de error



def listar_todos_los_centros():
    return list(collection.find({}, {"_id": 0}))









