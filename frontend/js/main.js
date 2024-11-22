// Importa el sistema de caché desde el módulo cache.js
import { pageCache } from './modules/cache.js';

// Objeto de configuración global con URL base de la API y número de filas por página
const CONFIG = {
    BASE_URL: "http://127.0.0.1:8000/api",
    ROWS_PER_PAGE: 12
};

// Variable global para controlar la página actual
let currentPage = 1;

// Cuando el DOM está completamente cargado, inicializa los event listeners y carga los tipos de centro
document.addEventListener('DOMContentLoaded', () => {
    initEventListeners();
    cargarTiposDeCentro();
});

// Inicializa los event listeners para el formulario y botones de paginación
function initEventListeners() {
    const formFiltros = document.getElementById("form-filtros");
    const prevButton = document.getElementById('prev-page');
    const nextButton = document.getElementById('next-page');
    const searchButton = document.getElementById('search-button');

    if (formFiltros) {
        // Agregar múltiples event listeners para mejor soporte móvil
        formFiltros.addEventListener("submit", handleFormSubmit);
        formFiltros.addEventListener("touchend", handleFormSubmit);
    }

    if (searchButton) {
        // Prevenir doble tap en móviles
        searchButton.addEventListener('touchend', (e) => {
            e.preventDefault();
            handleFormSubmit(e);
        });
    }

    if (prevButton) {
        prevButton.addEventListener('click', handlePrevPage);
        prevButton.addEventListener('touchend', handlePrevPage);
    }

    if (nextButton) {
        nextButton.addEventListener('click', handleNextPage);
        nextButton.addEventListener('touchend', handleNextPage);
    }document.getElementById("form-filtros").addEventListener("submit", handleFormSubmit);
    document.getElementById('prev-page').addEventListener('click', handlePrevPage);
    document.getElementById('next-page').addEventListener('click', handleNextPage);
}

// Maneja el envío del formulario: previene el comportamiento por defecto,
// resetea la página a 1 y carga los centros
async function handleFormSubmit(event) {
    event.preventDefault();
    
    // Prevenir múltiples envíos
    const submitButton = document.getElementById('search-button');
    if (submitButton) {
        submitButton.disabled = true;
    }

    try {
        currentPage = 1;
        await cargarCentros(currentPage);
        actualizarPaginacion();
    } catch (error) {
        console.error('Error al enviar formulario:', error);
    } finally {
        // Reactivar el botón después de procesar
        if (submitButton) {
            submitButton.disabled = false;
        }
    }
}

// Maneja el click en el botón "anterior": decrementa la página si es posible
async function handlePrevPage() {
    try {
        if (currentPage > 1) {
            currentPage--;
            await cargarCentros(currentPage);
            actualizarPaginacion();
        }
    } catch (error) {
        console.error('Error al navegar a la página anterior:', error);
    }
}

// Maneja el click en el botón "siguiente": incrementa la página
async function handleNextPage() {
    try {
        currentPage++;
        await cargarCentros(currentPage);
        actualizarPaginacion();
    } catch (error) {
        console.error('Error al navegar a la página siguiente:', error);
    }
}


// Realiza la petición HTTP a la API para obtener los centros
async function fetchCentros(params) {
    try {
        const response = await fetch(`${CONFIG.BASE_URL}/centros?${params.toString()}`);
        if (!response.ok) throw new Error("Error al obtener datos");
        const data = await response.json();
        return data.centros;
    } catch (error) {
        console.error("Error al obtener centros:", error);
        return [];
    }
}

// Función principal para cargar los centros con sistema de caché
async function cargarCentros(page) {
    mostrarLoadingIndicator(true);
    try {
        // Verifica si los datos están en caché
        const cachedData = pageCache.getPage(page);
        if (cachedData) {
            console.log(`Usando caché para página ${page}`);
            mostrarCentros(cachedData);
            return;
        }

        // Si no hay caché, carga los datos desde la API
        const params = obtenerParametrosBusqueda(page);
        const centros = await fetchCentros(params);
        mostrarCentros(centros);
        
        // Guarda los datos en caché
        pageCache.setPage(page, centros);
        
        // Precarga la siguiente página
        const nextPage = page + 1;
        const nextParams = obtenerParametrosBusqueda(nextPage);
        const nextCentros = await fetchCentros(nextParams);
        pageCache.setPage(nextPage, nextCentros);

    } catch (error) {
        console.error('Error al cargar centros:', error);
        mostrarCentros([]);
    } finally {
        mostrarLoadingIndicator(false);
    }
}

// Obtiene los parámetros del formulario para la búsqueda
function obtenerParametrosBusqueda(page) {
    return new URLSearchParams({
        localidad: document.getElementById("localidad").value || '',
        etapa: document.getElementById("etapa").value || '',
        provincia: document.getElementById("provincia").value || '',
        codigo: document.getElementById("codigo").value || '',
        nombreCentro: document.getElementById("nombreCentro").value || '',
        tipoCentro: document.getElementById("tipoCentro").value || '',
        direccionOrigen: document.getElementById("direccionOrigen").value || '',
        page,
        rowsPerPage: CONFIG.ROWS_PER_PAGE
    });
}

// Muestra u oculta el indicador de carga
function mostrarLoadingIndicator(show) {
    const loadingIndicator = document.getElementById("loading-indicator");
    if (loadingIndicator) {
        loadingIndicator.style.display = show ? "block" : "none";
    }
}

// Actualiza los elementos de paginación en la UI
function actualizarPaginacion() {
    document.getElementById('current-page').textContent = currentPage;
    document.getElementById('prev-page').disabled = currentPage === 1;
}

// Muestra los centros en la tabla
export function mostrarCentros(centros) {
    const tabla = document.getElementById("tabla-centros");
    tabla.innerHTML = "";

    // Si no hay resultados, muestra mensaje
    if (centros.length === 0) {
        tabla.innerHTML = "<tr><td colspan='7'>No se encontraron resultados</td></tr>";
        return;
    }
    
    // Crea una fila por cada centro
    centros.forEach(centro => {
        const fila = document.createElement("tr");
        fila.innerHTML = `
            <td>${centro.codigo || "Sin código"}</td>            
            <td>${centro.D_DENOMINA+" "+centro.D_ESPECIFICA || "Sin nombre"}</td>
            <td>${centro.D_DOMICILIO || "Sin dirección"}</td>
            <td>${centro.C_POSTAL || "Sin CP"}</td>
            <td>${centro.D_LOCALIDAD || "Sin localidad"}</td>
            <td>${centro.D_PROVINCIA || "Sin provincia"}</td>
            <td>${"Distancia: "+ centro.distancia+" Duración: " +centro.duracion || "No se pudo calcular"}</td>
        `;
        tabla.appendChild(fila);
    });
}

// Carga los tipos de centro disponibles
export async function cargarTiposDeCentro() {
    try {        
        // Obtiene los tipos de centro desde la API
        const response = await fetch(`${CONFIG.BASE_URL}/centros/tipos`);
        if (!response.ok) throw new Error("Error al cargar los tipos de centro");
        const data = await response.json();
        const select = document.getElementById("tipoCentro");

        // Crea las opciones del select
        data.tipos.forEach(tipo => {
            const option = document.createElement("option");
            option.value = tipo;
            option.textContent = tipo;
            select.appendChild(option);
        });
    } catch (error) {
        console.error("Error al cargar tipos de centro:", error);
    }
}