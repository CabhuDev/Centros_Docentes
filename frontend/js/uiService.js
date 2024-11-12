/**
 * Inicializa los headers de la tabla desde el primer objeto de datos
 * @param {Array} datos - Array de centros educativos
 */
function inicializarHeaders(datos) {
    if (datos && datos.length > 0) {
        // Obtener las claves del primer objeto
        const headers = Object.keys(datos[0]);
        
        // Crear elemento thead si no existe
        let thead = document.querySelector("#centros-table thead");
        if (!thead) {
            thead = document.createElement("thead");
            document.querySelector("#centros-table").appendChild(thead);
        }
        
        // Crear fila de headers
        const headerRow = document.createElement("tr");
        
        // Crear y añadir las celdas de header
        headers.forEach(header => {
            const th = document.createElement("th");
            th.textContent = header;
            headerRow.appendChild(th);
            
            // Actualizar objeto COLUMNAS dinámicamente
            COLUMNAS[header.toUpperCase().replace(/\s+/g, '_')] = header;
        });
        
        // Limpiar y añadir nueva fila de headers
        thead.innerHTML = "";
        thead.appendChild(headerRow);
    }
}



/**
 * Crea una celda de tabla con el contenido especificado
 * @param {string} contenido - Texto a mostrar en la celda
 * @returns {HTMLElement} Elemento TD creado
 */
function crearCeldaTabla(contenido) {
    const celda = document.createElement("td");
    if (contenido === "Es bilingüe" || contenido === "Es compensatorio") {
        celda.style.fontWeight = "bold";
        celda.style.color = "red";
    }
    celda.textContent = contenido || '-'; // Si no hay contenido, mostrar guión
    return celda;
}

/**
 * Función crearFilaCentro modificada para usar headers dinámicos
 */
function crearFilaCentro(centro) {
    const fila = document.createElement("tr");
    
    // Crear celdas usando todas las propiedades del objeto
    const celdas = Object.keys(centro).map(key => 
        crearCeldaTabla(centro[key])
    );
    
    celdas.forEach(celda => fila.appendChild(celda));
    return fila;
}


/**
 * Muestra los datos en la tabla
 * @param {Array} datos - Array de centros educativos
 */
function mostrarDatosEnTabla(datos) {
    const tableBody = document.querySelector("#centros-table tbody");
    tableBody.innerHTML = ""; // Limpiar tabla

    datos.forEach(centro => {
        const fila = crearFilaCentro(centro);
        tableBody.appendChild(fila);
    });
}

/**
 * Muestra mensajes de error en la consola y opcionalmente en la UI
 * @param {Error} error - Error ocurrido
 */
function mostrarError(error) {
    console.error("Error al cargar los datos:", error);
    
    // Opcional: Mostrar error al usuario
    const tableBody = document.querySelector("#centros-table tbody");
    tableBody.innerHTML = `
        <tr>
            <td colspan="4" class="error-message">
                Error al cargar los datos. Por favor, intente más tarde.
            </td>
        </tr>
    `;
}