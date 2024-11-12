// Esperar a que el documento esté listo
document.addEventListener("DOMContentLoaded", inicializarTabla);

/**
 * Inicializa la tabla de datos obteniendo datos de centros, configurando filtros y mostrando la información.
 * Esta función maneja la configuración inicial del componente de tabla incluyendo:
 * - Obtención de datos desde la API de centros
 * - Creación de copias de respaldo de los datos originales y filtrados
 * - Configuración de filtros de encabezado
 * - Inicialización de encabezados de tabla
 * - Visualización de los datos filtrados en la tabla
 * 
 * @async
 * @function inicializarTabla
 * @throws {Error} Lanzará un error si falla la obtención de datos o la inicialización de la tabla
 * @returns {Promise<void>}
 */
async function inicializarTabla() {
    try {
        const datos = await obtenerDatosCentros();
        datosOriginales = [...datos];
        datosFiltrados = [...datos];
        
        crearFiltrosCabecera(datos);
        inicializarHeaders(datos);
        mostrarDatosEnTabla(datosFiltrados);
    } catch (error) {
        mostrarError(error);
    }
}

document.addEventListener("DOMContentLoaded", muestraImagen)
function muestraImagen() {
    const loadImageButton = document.getElementById("load-image-btn");
    const imageElement = document.getElementById("imagen-risa");

    loadImageButton.addEventListener("click", async () => {
        try {
            const imageBlob = await obtenerImagen();
            if (imageBlob) {
                const imageUrl = URL.createObjectURL(imageBlob);
                imageElement.src = imageUrl;
                imageElement.style.display = "block";
            }
        } catch (error) {
            console.error("Error al cargar la imagen:", error);
        }
    });

}











