import { obtenerCentros, cargarTiposDeCentro } from "./apiService.js";
import { mostrarCentros, rellenarTiposDeCentro } from "./uiService.js";

/**
 * Configura los eventos de los formularios y botones.
 */
export function configurarEventos() {
    document.getElementById("form-filtros").addEventListener("submit", async (event) => {
        event.preventDefault();

        const codigo = document.getElementById("codigo").value;
        const nombreCentro = document.getElementById("nombreCentro").value;
        const localidad = document.getElementById("localidad").value;
        const etapa = document.getElementById("etapa").value;
        const provincia = document.getElementById("provincia").value;
        const tipoCentro = document.getElementById("tipoCentro").value;
        const direccionOrigen = document.getElementById("direccionOrigen").value;
        console.log("Tipo de Centro enviado:", tipoCentro);
        
        const centros = await obtenerCentros(localidad, etapa, provincia, codigo, nombreCentro, tipoCentro, direccionOrigen);
        mostrarCentros(centros);
    });

    // Cargar tipos de centro al inicio
    cargarTiposDeCentro().then(rellenarTiposDeCentro).catch(console.error);
}


