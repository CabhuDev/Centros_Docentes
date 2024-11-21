// modules/ui.js
export function mostrarCentros(centros) {
    const tableBody = document.querySelector('table tbody');
    tableBody.innerHTML = '';

    centros.forEach(centro => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${centro.codigo}</td>
            <td>${centro.nombre}</td>
            <td>${centro.direccion}</td>
            <td>${centro.codigoPostal}</td>
            <td>${centro.localidad}</td>
            <td>${centro.provincia}</td>
            <td>${centro.etapa}</td>
        `;
        tableBody.appendChild(row);
    });
}

export function actualizarPaginacion(currentPage, hasMore) {
    document.getElementById('current-page').textContent = currentPage;
    document.getElementById('prev-page').disabled = currentPage === 1;
    document.getElementById('next-page').disabled = !hasMore;
}