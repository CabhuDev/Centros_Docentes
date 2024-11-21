// modules/api.js
import { CONFIG } from '../config.js';

export async function fetchTiposCentro() {
    const response = await fetch(`${CONFIG.BASE_URL}/centros/tipos`);
    if (!response.ok) throw new Error("Error al cargar los tipos de centro");
    return response.json();
}

export async function fetchCentros(params) {
    const queryParams = new URLSearchParams(params);
    const response = await fetch(`${CONFIG.BASE_URL}/centros?${queryParams}`);
    if (!response.ok) throw new Error("Error al cargar centros");
    return response.json();
}