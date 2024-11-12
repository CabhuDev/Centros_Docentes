# Geocodificación del Origen (si el usuario introduce una dirección): 
# Utiliza la API de geocodificación de Google Maps para convertir la dirección del usuario en coordenadas. 
# Esta conversión es necesaria si el usuario introduce una dirección en lugar de coordenadas.

import googlemaps
import googlemaps.distance_matrix
import googlemaps.geocoding
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")


def obtener_coordenadas(direccion_usuario: str) -> tuple:
    """
    Convierte una dirección en coordenadas geográficas (latitud, longitud).
    
    Args:
        direccion_usuario (str): Dirección postal completa a geocodificar
        
    Returns:
        tuple: Par de coordenadas (latitud, longitud) o (None, None) si hay error
        
    Raises:
        Exception: Si hay error en la comunicación con la API de Google Maps
    """
    try:
        # Inicializar cliente de Google Maps con la clave API
        gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)
        
        # Geocodificar la dirección para obtener coordenadas
        geocode_result = googlemaps.geocoding.geocode(gmaps, direccion_usuario)
        
        if geocode_result:
            # Extraer coordenadas del primer resultado
            # Google Maps puede devolver múltiples resultados, tomamos el primero
            lat = geocode_result[0]['geometry']['location']['lat']
            lng = geocode_result[0]['geometry']['location']['lng']
            print(f"Coordenadas obtenidas: {lat}, {lng}")
            return lat, lng
        else:
            print("No se pudieron obtener coordenadas para la dirección proporcionada.")
    except Exception as e:
        print(f"Error al obtener coordenadas: {e}")

    return None, None


def calcular_distancias(direccion_origen: str, direccion_destino: str) -> dict:
    """
    Calcula la distancia y tiempo de viaje entre dos direcciones usando Google Maps.
    
    Args:
        direccion_origen (str): Dirección del punto de partida
        direccion_destino (str): Dirección del punto de llegada
        
    Returns:
        dict: Diccionario con distancia en km, metros y duración del trayecto.
              Retorna diccionario vacío si hay error.
        
    Ejemplo de retorno:
        {
            "distancia en Km": "10 km",
            "distancia en m": 10000,
            "duracion": "15 mins"
        }
    """
    try:
        # Inicializar cliente de Google Maps
        gmaps = googlemaps.Client(GOOGLE_MAPS_API_KEY)

        # Consultar matriz de distancia
        # mode="driving" indica cálculo para vehículos
        # language="ES" obtiene resultados en español
        result = googlemaps.distance_matrix.distance_matrix(
            gmaps,
            origins=direccion_origen, 
            destinations=direccion_destino,
            language="ES", 
            mode="driving"
        )
        
        # Verificar si hay resultados válidos
        if (result['rows'] and 
            result['rows'][0]['elements'] and 
            result['rows'][0]['elements'][0]['status'] == 'OK'):
            
            # Extraer datos del resultado
            distancia_km = result['rows'][0]['elements'][0]['distance']['text']
            distancia_value = result['rows'][0]['elements'][0]['distance']['value']
            duracion = result['rows'][0]['elements'][0]['duration']['text']
            
            # Retornar diccionario con los datos
            return {
                "distancia en Km": distancia_km,
                "distancia en m": distancia_value,
                "duracion": duracion
            }
        else:
            print("No se pudo calcular la distancia para las direcciones proporcionadas.")
    except Exception as e:
        print(f"Error al calcular la distancia: {e}")
        
    return {}


#-- PRUEBA DE LAS FUNCIONES --#

"""direccion_origen = "Calle Costa Rica 49, 18194, Churriana de la Vega, Granada"
direccion_destino = " Cordoba,14700651C, I.E.S. Ricardo Delgado Vizcaíno"
coordenadas_origen = obtener_coordenadas(direccion_origen)
coordenadas_destino = obtener_coordenadas(direccion_destino)
print("------------------")
print(coordenadas_origen)
print(coordenadas_destino)

#IES JOSE MARÍN
lat_test = 37.65969
lng_test = -2.07848
destino = f"{lat_test},{lng_test}"
print (destino)

print("------------------")
print(calcular_distancias(direccion_origen,direccion_destino))
"""