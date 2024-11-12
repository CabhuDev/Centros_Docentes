/**
 * Obtiene los datos de los centros desde la API
 * @returns {Promise} Datos de los centros
 */
async function obtenerDatosCentros() {
    const response = await fetch(API_CONFIG.URL);
    if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
    }
    return await response.json();
}


/**
 * Obtiene una imagen desde el endpoint del servidor local.
 * @async
 * @function obtenerImagen
 * @returns {Promise<Blob>} Una promesa que se resuelve con un Blob conteniendo los datos de la imagen
 * @throws {Error} Si hay un problema al obtener la imagen del servidor
 */
async function obtenerImagen() {
    try {
        const response = await fetch("http://localhost:8000/image");
        if (!response.ok) {
            throw new Error('Error al cargar la imagen');
        }
        return await response.blob();
    } catch (error) {
        console.error("Hubo un problema al obtener la imagen:", error);
    }
}
