function ordenarCentros(criterio, orden = "asc") {
    centros.sort((a, b) => {
        let valorA = a[criterio] || 0;
        let valorB = b[criterio] || 0;

        if (criterio === "distancia") {
            valorA = parseFloat(a[criterio]);
            valorB = parseFloat(b[criterio]);
        }

        if (orden === "asc") {
            return valorA - valorB;
        } else {
            return valorB - valorA;
        }
    });
    mostrarCentros(centros); // Re-renderizar la tabla
}
