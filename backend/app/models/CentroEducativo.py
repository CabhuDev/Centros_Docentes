from services.googleConnect import calcular_distancias
import re

class CentroEducativo:
    def __init__(self, direccion,codigo_postal, municipio, provincia,codigo_centro,tipo_centro,nombre_centro,publico_privado,bil,compensatoria):
        """
        Initialize a CentroEducativo (Educational Center) object with its basic attributes.
        Args:
            direccion (str): Street address of the educational center
            codigo_postal (str): Postal code of the center's location
            municipio (str): Municipality where the center is located
            provincia (str): Province where the center is located
            codigo_centro (str): Unique identifier code for the educational center
            tipo_centro (str): Type of educational center (e.g., Primary, Secondary)
            nombre_centro (str): Official name of the educational center
            publico_privado (str): Indicates if the center is public or private
            bil (bool): Indicates if the center is bilingual
            compensatoria (bool): Indicates if the center has compensatory education programs
        Attributes:
            All the parameters above become instance attributes, plus:
            distancia_km (float, optional): Distance in kilometers (initialized as None)
            distancia_m (float, optional): Distance in meters (initialized as None)
            duracion (float, optional): Travel duration (initialized as None)
        """

        self.direccion = direccion
        self.codigo_postal = codigo_postal
        self.municipio = municipio
        self.provincia = provincia
        self.codigo_centro = codigo_centro
        self.nombre_centro = nombre_centro
        self.tipo_centro = tipo_centro
        self.publico_privado = publico_privado
        self.bil = bil
        self.compensatoria = compensatoria
        self.distancia_km = None
        self.distancia_m = None
        self.duracion = None

    def __repr__(self):
        """
        Método especial que devuelve una representación en string del objeto CentroEducativo.
        Se usa principalmente para debugging y desarrollo.
        
        Returns:
            str: Representación del centro educativo con su nombre y código
        """
        return f"CentroEducativo({self.nombre_centro}, {self.codigo_centro})"
    
    
    def calcula_distancia_clase(self, direccion_origen):
        """
        Calcula la distancia y duración del trayecto desde una dirección origen hasta el centro educativo.

        Args:
            direccion_origen (str): Dirección desde donde se calculará la distancia

        Returns:
            bool: True si el cálculo fue exitoso, False si hubo algún error

        Note:
            Actualiza los atributos distancia_km, distancia_m y duracion del centro
            usando el servicio de Google Maps
        """
        # Construir la dirección completa de destino combinando los elementos
        direccion_destino = f"{self.direccion},{self.codigo_postal}, {self.municipio}, {self.provincia}"
        
        # Llamar al servicio externo de Google para calcular distancias y tiempos
        resultado = calcular_distancias(direccion_origen, direccion_destino)
        
        # Procesar el resultado si existe
        if resultado:
            # Actualizar los atributos del centro con los valores calculados
            self.distancia_km = resultado['distancia en Km']
            self.distancia_m = resultado['distancia en m']
            self.duracion = resultado['duracion']
            return True
        else:
            # En caso de error al calcular, mostrar mensaje y retornar False
            print(f"No se pudo calcular la distancia para el destino: {direccion_destino}")
            return False

    @staticmethod
    def convertir_duracion_a_minutos(duracion_str):
        """
        Convierte una cadena de texto que representa una duración en formato 'Xh Ymin' a minutos totales.

        Args:
            duracion_str (str): String con el formato 'Xh Ymin' (ej: '2h 15min' o '45min')

        Returns:
            int: Total de minutos calculados

        Example:
            >>> CentroEducativo.convertir_duracion_a_minutos('2h 15min')
            135
            >>> CentroEducativo.convertir_duracion_a_minutos('45min')
            45
        """
        # Busca patrones de números seguidos de 'h' o 'min' en el string
        partes = re.findall(r'(\d+)\s*(h|min)', duracion_str)
        
        # Inicializa el contador de minutos
        total_minutos = 0
        
        # Recorre cada parte encontrada (valor y unidad)
        for valor, unidad in partes:
            valor = int(valor)
            if unidad == 'h':
                # Si la unidad es horas, multiplica por 60 para convertir a minutos
                total_minutos += valor * 60
            elif unidad == 'min':
                # Si la unidad es minutos, suma directamente
                total_minutos += valor
                
        return total_minutos
