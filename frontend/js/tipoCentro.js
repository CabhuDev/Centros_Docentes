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
async function cargarTiposDeCentro() {
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