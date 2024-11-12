/**
 * Configuración de la aplicación
 * Contiene las constantes globales y configuración de la API
 */
const API_CONFIG = {
    URL: "http://localhost:8000/api/centros",
    HEADERS: {
        'Content-Type': 'application/json'
    }
};

/**
 * Mapeo de nombres de columnas
 * Define la estructura y nombres de las columnas que se mostrarán en la tabla
 */
let COLUMNAS = {
    CODIGO: 'Código Centro',
    NOMBRE: 'Nombre Centro',
    MUNICIPIO: 'Municipio',
    PROVINCIA: 'Provincia',
    MODALIDAD: 'Idiomas',
    DISTANCIA_A_DESTINO: 'Distancia (Km)',
    DURACION_TRAYECTO: 'Duración',
    TIPO_CENTRO: 'Centro Compensatorio'
};