// Variables globales
let datosOriginales = []; // Almacenar datos sin filtrar
let datosFiltrados = []; // Almacenar datos filtrados

/**
 * Crea el selector de provincias
 */
/**
 * Crea y configura un menú desplegable de filtro de provincias encima de la tabla de centros.
 * Esta función genera un elemento select con todas las provincias únicas de los datos originales,
 * lo añade a un contenedor y lo coloca antes de la tabla de centros.
 * El desplegable incluye una opción predeterminada "Todas las provincias" y nombres de provincias ordenados.
 * Cuando se selecciona una provincia, activa la función filtrarPorProvincia.
 * 
 * @function crearFiltroProvincia
 * @requires datosOriginales - Array global que contiene los datos de los centros
 * @requires filtrarPorProvincia - Función para manejar el filtrado por provincia
 * @returns {void}
 */
function crearFiltroProvincia() {
    // Crear contenedor
    const filterContainer = document.createElement('div');
    filterContainer.className = 'filter-container';
    
    // Crear select
    const select = document.createElement('select');
    select.id = 'provincia-filter';
    
    // Opción por defecto
    const defaultOption = document.createElement('option');
    defaultOption.value = '';
    defaultOption.textContent = 'Todas las provincias';
    select.appendChild(defaultOption);
    
    // Obtener provincias únicas
    const provincias = [...new Set(datosOriginales.map(centro => centro["Provincia"]))];
    
    // Agregar opciones
    provincias.sort().forEach(provincia => {
        const option = document.createElement('option');
        option.value = provincia;
        option.textContent = provincia;
        select.appendChild(option);
    });
    
    // Evento de cambio
    select.addEventListener('change', filtrarPorProvincia);
    
    filterContainer.appendChild(select);
    document.querySelector('#centros-table').before(filterContainer);
}

/**
 * Filtra los datos por provincia seleccionada
 * 
 * @function filtrarPorProvincia
 * @description
 * Esta función:
 * 1. Obtiene la provincia seleccionada del selector
 * 2. Filtra los datos originales si hay una provincia seleccionada
 * 3. Si no hay provincia seleccionada, usa todos los datos originales
 * 4. Actualiza la tabla con los datos filtrados
 * 
 * @example
 * // Cuando el usuario selecciona una provincia en el selector
 * filtrarPorProvincia();
 */
function filtrarPorProvincia() {
    // Obtener valor seleccionado del filtro de provincia
    const provinciaSeleccionada = document.querySelector('#provincia-filter').value;
    
    // Filtrar datos o usar todos si no hay selección
    datosFiltrados = provinciaSeleccionada 
        ? datosOriginales.filter(centro => centro['Provincia'] === provinciaSeleccionada)
        : [...datosOriginales];
    
    // Actualizar la visualización de la tabla
    mostrarDatosEnTabla(datosFiltrados);
}


/**
 * Crea los filtros en la cabecera
 */
/**
 * Crea y configura filtros en la cabecera de la tabla para diferentes columnas
 * @param {Array<Object>} datos - Array de objetos que contiene los datos de los centros educativos
 * 
 * @description
 * Esta función realiza lo siguiente:
 * 1. Crea un contenedor para los filtros
 * 2. Define las columnas que se podrán filtrar
 * 3. Para cada columna:
 *    - Crea un grupo de filtro con etiqueta y selector
 *    - Añade una opción por defecto "Todos"
 *    - Obtiene valores únicos de los datos para esa columna
 *    - Crea opciones para cada valor único
 *    - Configura el evento de cambio
 * 4. Inserta los filtros antes de la tabla
 * 
 * @example
 * // Asumiendo que tienes un array de datos de centros:
 * const datosCentros = [
 *   { Municipio: "Sevilla", Provincia: "Sevilla", "Centro Compensatorio": "Sí", Idiomas: "Inglés" },
 *   // ... más datos
 * ];
 * crearFiltrosCabecera(datosCentros);
 */
function crearFiltrosCabecera(datos) {
    // Crear contenedor principal
    const filterContainer = document.createElement('div');
    filterContainer.className = 'filters-header';

    // Definir columnas para filtrar
    const columnasFiltrar = ['Municipio', 'Provincia', 'Centro Compensatorio', 'Idiomas'];

    // Crear filtros para cada columna
    columnasFiltrar.forEach(columna => {
        const filterGroup = document.createElement('div');
        filterGroup.className = 'filter-group';

        const label = document.createElement('label');
        label.textContent = columna;

        const select = document.createElement('select');
        select.id = `filter-${columna.toLowerCase().replace(/\s+/g, '-')}`;
        select.className = 'header-filter';

        // Opción por defecto
        const defaultOption = document.createElement('option');
        defaultOption.value = '';
        defaultOption.textContent = `Todos ${columna}`;
        select.appendChild(defaultOption);

        // Obtener valores únicos para el filtro
        const valores = [...new Set(datos.map(item => item[columna]))];
        valores.sort().forEach(valor => {
            const option = document.createElement('option');
            option.value = valor;
            option.textContent = valor;
            select.appendChild(option);
        });

        // Evento de cambio
        select.addEventListener('change', aplicarFiltros);

        filterGroup.appendChild(label);
        filterGroup.appendChild(select);
        filterContainer.appendChild(filterGroup);
    });

    // Insertar antes de la tabla
    document.querySelector('#centros-table').before(filterContainer);
}

/**
 * Aplica todos los filtros seleccionados
 * 
 * Esta función aplica filtros al conjunto de datos original basándose en los criterios 
 * seleccionados por el usuario y actualiza la visualización de la tabla.
 * Los filtros se aplican por municipio, provincia, estado compensatorio e idiomas.
 * 
 * @function aplicarFiltros
 * @returns {void} Actualiza la variable global datosFiltrados y refresca la tabla
 * 
 * @example
 * // Llamar a la función cuando cambien los valores de los filtros
 * aplicarFiltros();
 * 
 * @description
 * La función:
 * 1. Recopila los valores de los filtros desde elementos del DOM
 * 2. Filtra el conjunto de datos original (datosOriginales) según los criterios
 * 3. Actualiza la visualización de la tabla con los resultados filtrados
 * Los valores de filtro vacíos se ignoran (se tratan como "mostrar todo")
 */
function aplicarFiltros() {
    const filtros = {
        municipio: document.querySelector('#filter-municipio').value,
        provincia: document.querySelector('#filter-provincia').value,
        compensatorio: document.querySelector('#filter-centro-compensatorio').value,
        idiomas: document.querySelector('#filter-idiomas').value
    };

    datosFiltrados = datosOriginales.filter(centro => {
        return (!filtros.municipio || centro['Municipio'] === filtros.municipio) &&
               (!filtros.provincia || centro['Provincia'] === filtros.provincia) &&
               (!filtros.compensatorio || centro['Centro Compensatorio'] === filtros.compensatorio) &&
               (!filtros.idiomas || centro['Idiomas'] === filtros.idiomas);
    });

    mostrarDatosEnTabla(datosFiltrados);
}