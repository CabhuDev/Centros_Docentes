// cache.js
export class PaginationCache {
    constructor() {
        this.cache = new Map();
        this.loading = new Set();
        this.timeToLive = 5 * 60 * 1000; // 5 minutos
    }

    setPage(page, data) {
        this.cache.set(page, {
            data,
            timestamp: Date.now()
        });
    }

    getPage(page) {
        const cached = this.cache.get(page);
        if (!cached) return null;

        // Verificar si el caché ha expirado
        if (Date.now() - cached.timestamp > this.timeToLive) {
            this.cache.delete(page);
            return null;
        }

        return cached.data;
    }

    isLoading(page) {
        return this.loading.has(page);
    }

    setLoading(page) {
        this.loading.add(page);
    }

    clearLoading(page) {
        this.loading.delete(page);
    }

    clear() {
        this.cache.clear();
        this.loading.clear();
    }

    async precargarPaginas(currentPage, obtenerCentros, formData) {
        const pagesToPreload = [currentPage + 1, currentPage + 2];

        for (const page of pagesToPreload) {
            if (!this.getPage(page) && !this.isLoading(page)) {
                this.setLoading(page);
                try {
                    const centros = await obtenerCentros(
                        formData.localidad,
                        formData.etapa,
                        formData.provincia,
                        formData.codigo,
                        formData.nombreCentro,
                        formData.tipoCentro,
                        formData.direccionOrigen,
                        page,
                        formData.rowsPerPage
                    );
                    this.setPage(page, centros);
                    console.log(`Página ${page} precargada`);
                } catch (error) {
                    console.error(`Error al precargar página ${page}:`, error);
                } finally {
                    this.clearLoading(page);
                }
            }
        }
    }
}

// Exportar instancia única del caché
export const pageCache = new PaginationCache();