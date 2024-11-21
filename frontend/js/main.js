// URL base de la API
const BASE_URL = "http://127.0.0.1:8000/api";
let currentPage = 1;
let rowsPerPage = 10;

// Escuchar el envío del formulario
document.getElementById("form-filtros").addEventListener("submit", async (event) => {
    event.preventDefault();
    /*------------------------*/
    currentPage = 1; // Reinicia la página actual al enviar el formulario
    await cargarCentros(currentPage);
    actualizarPaginacion();
})

document.getElementById('prev-page').addEventListener('click', async function() {
    if (currentPage > 1) {
        currentPage--;
        await cargarCentros(currentPage);
        actualizarPaginacion();
    }
}); 

document.getElementById('next-page').addEventListener('click', async function() {
    currentPage++;
    await cargarCentros(currentPage);
    actualizarPaginacion();
});


/**
 * Obtiene centros educativos desde la API con filtros opcionales.
 * @param {string} localidad - Nombre de la localidad para filtrar
 * @param {string} etapa - Tipo de etapa educativa (ESO, etc)
 * @param {string} provincia - Nombre de la provincia para filtrar
 * @param {string} codigo - Código del centro educativo
 * @param {string} nombreCentro - Nombre del centro para buscar
 * @returns {Promise<Array>} Array de objetos con información de centros educativos
 * @throws {Error} Si hay un error en la petición a la API
 */
export async function obtenerCentros(
                            localidad, 
                            etapa, 
                            provincia,
                            codigo,
                            nombreCentro ,
                            tipoCentro ,
                            direccionOrigen,
                            page,
                            rowsPerPage) {
                    
    try {

        // Mostrar el icono de carga
        let loadingIndicator = document.getElementById("loading-indicator");
        if (loadingIndicator) loadingIndicator.style.display = "block";


        // Construye la URL base para la solicitud
        let url = `${BASE_URL}/centros`;
    
        // Crea un objeto URLSearchParams para manejar los parámetros de la URL
        let params = new URLSearchParams({
            localidad: localidad || '',
            etapa: etapa || '',
            provincia: provincia || '',
            codigo: codigo || '',
            nombreCentro: nombreCentro || '',
            tipoCentro: tipoCentro || '',
            direccionOrigen: direccionOrigen || '',
            page,
            rowsPerPage
        });
            
        const response = await fetch(`${BASE_URL}/centros?${params.toString()}`);
    
        // Verifica si la respuesta no es exitosa (código de estado no en el rango 200-299)
        if (!response.ok) {
            // Lanza un error si la respuesta no es exitosa
            throw new Error("Error al obtener datos");
        }
    
        // Convierte la respuesta a formato JSON
        let data = await response.json();
    
        // Retorna la lista de centros obtenida de los datos
        //return data.centros;
        return data.centros;
    } catch (error) {
        // Captura cualquier error ocurrido durante el proceso
        console.error("Error al obtener centros:", error);

        // Ocultar el icono de carga en caso de error
        let loadingIndicator = document.getElementById("loading-indicator");
        if (loadingIndicator) loadingIndicator.style.display = "none";
    
        // Retorna un arreglo vacío en caso de error
        return [];
    }
}

/*----------------------------CACHEO DE DATOS-----------------------------------*/
// Función de debounce para evitar múltiples llamadas
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Cache para almacenar resultados
const cache = new Map();
const CACHE_TIME = 5 * 60 * 1000; // 5 minutos
/*----------------------------CACHEO DE DATOS-----------------------------------*/

// Función para cargar datos paginados
async function cargarCentros(page) {
    // Obtener elementos del formulario directamente
    let codigo = document.getElementById("codigo").value;
    let nombreCentro = document.getElementById("nombreCentro").value;
    let localidad = document.getElementById("localidad").value;
    let etapa = document.getElementById("etapa").value;
    let provincia = document.getElementById("provincia").value;
    let tipoCentro = document.getElementById("tipoCentro").value;
    let direccionOrigen = document.getElementById("direccionOrigen").value;

    let centros = await obtenerCentros(localidad, etapa, provincia, codigo, nombreCentro, tipoCentro, direccionOrigen, page, rowsPerPage);
    mostrarCentros(centros);
}



function actualizarPaginacion() {
    document.getElementById('current-page').textContent = currentPage;
    document.getElementById('prev-page').disabled = currentPage === 1;
    // Aquí podrías agregar lógica adicional para deshabilitar el botón "Siguiente" si no hay más resultados
}



/**
 * Muestra los centros en la tabla del DOM.
 */

/**
 * Función para mostrar centros en la tabla del HTML.
 * Muestra una lista de centros educativos en una tabla HTML
 * @param {Array} centros - Array de objetos que contienen información de centros educativos
 * @param {string} centros[].codigo - Código de identificación del centro
 * @param {string} centros[].D_ESPECIFICA - Nombre del centro
 * @param {string} centros[].D_DOMICILIO - Dirección del centro
 * @param {string} centros[].D_LOCALIDAD - Ciudad donde se encuentra el centro
 * @param {string} centros[].D_PROVINCIA - Provincia donde se encuentra el centro
 * @param {string} centros[].ESO - Indica si el centro ofrece educación ESO ("Yes"/"No")
 * @returns {void} - No devuelve nada, actualiza el DOM directamente
 * @description 
 * La función limpia cualquier contenido existente en la tabla y la rellena con los datos de centros proporcionados.
 * Si el array de centros está vacío, muestra un mensaje de "No se encontraron resultados".
 * Para cualquier campo de datos faltante, muestra "Sin [nombre del campo]" como texto predeterminado.
 */
export function mostrarCentros(centros) {
    // Obtiene la referencia a la tabla del DOM usando su ID
    let tabla = document.getElementById("tabla-centros");
    
    // Limpia el contenido actual de la tabla
    tabla.innerHTML = ""; 
    

    // Oculta el icono de carga
    let loadingIndicator = document.getElementById("loading-indicator");
    if (loadingIndicator) {
        loadingIndicator.style.display = "none";
    }

    // Si no hay centros que mostrar, muestra un mensaje de "No se encontraron resultados"
    if (centros.length === 0) {
        tabla.innerHTML = "<tr><td colspan='8'>No se encontraron resultados</td></tr>";
        return;
    }

    // Itera sobre cada centro en el array de centros
    centros.forEach(centro => {
        // Crea un nuevo elemento tr (fila) para cada centro
        let fila = document.createElement("tr");
        
        // Rellena la fila con los datos del centro
        // Usa el operador || para mostrar un texto por defecto si el dato no existe
        fila.innerHTML = `
            <td>${centro.codigo || "Sin código"}</td>            
            <td>${centro.D_DENOMINA+" "+centro.D_ESPECIFICA || "Sin nombre"}</td>
            <td>${centro.D_DOMICILIO || "Sin dirección"}</td>
            <td>${centro.C_POSTAL || "Sin CP"}</td>
            <td>${centro.D_LOCALIDAD || "Sin localidad"}</td>
            <td>${centro.D_PROVINCIA || "Sin provincia"}</td>
            <td>${centro.ESO === "Yes" ? "Sí" : "No"}</td>
            <td>${"Distancia: "+ centro.distancia+" Duración: " +centro.duracion || "No se pudo calcular"}</td>
        `;

        
        // Añade la fila completa a la tabla
        tabla.appendChild(fila);

        
    });
}



/**
 * Carga de forma asíncrona los tipos de centros desde el servidor y rellena un elemento select con los datos recuperados.
 * 
 * Obtiene los tipos de centros desde el endpoint `${BASE_URL}/centros/tipos` y añade cada tipo como una opción
 * al elemento select con el ID "tipoCentro".
 * 
 * @async
 * @function cargarTiposDeCentro
 * @throws Lanzará un error si la petición falla o la respuesta no es satisfactoria.
 */
export async function cargarTiposDeCentro() {
    // Construye la URL base para la solicitud
    let url = `${BASE_URL}/centros/tipos`;
    try {        
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error("Error al cargar los tipos de centro");
        }
        let data = await response.json();
        let select = document.getElementById("tipoCentro");

        data.tipos.forEach(tipo => {
            let option = document.createElement("option");
            option.value = tipo;
            option.textContent = tipo;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Error al cargar tipos de centro:", error);
    }
}

// Llama a la función al cargar la página
cargarTiposDeCentro();







