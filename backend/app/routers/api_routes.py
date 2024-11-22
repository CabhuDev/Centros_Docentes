from fastapi import APIRouter, Query
from backend.app.services.consultasMongo import *
from backend.app.services.googleConnect import *

router = APIRouter()


@router.get("/centros")
async def listar_centros(
    page: int = Query(1, ge=1),                     # Página actual
    rowsPerPage: int = Query(10, ge=1, le=100),      # Filas por página
    localidad: str = Query(None), 
    etapa: str = Query(None),
    provincia: str = Query(None),
    codigo: str = Query(None),
    nombreCentro: str = Query(None),
    tipoCentro: str = Query(None),
    codigoPostal: str = Query(None),
    direccionOrigen: str = Query(None)):  # Dirección de origen para calcular distancias


    """
    Endpoint para listar centros educativos con filtros y paginación.
    """
    try:
        # Verifica si alguno de los parámetros de filtro ha sido proporcionado
        if localidad or etapa or provincia or codigo or nombreCentro or tipoCentro:
            # Si se proporcionó al menos un filtro, llama a la función para obtener los centros filtrados
            centros = obtener_centros_filtrados(localidad,
                                                etapa,
                                                provincia,
                                                codigo,
                                                nombreCentro,                                             
                                                tipoCentro)
        else:
            # Si no se proporcionó ningún filtro, lista todos los centros
            centros = listar_todos_los_centros()


        # Calcular distancias si se proporciona una dirección de origen
        if direccionOrigen:
            for centro in centros:
                direccionDestino = f"{centro['D_DENOMINA']}, {centro['D_ESPECIFICA']}, {centro['D_DOMICILIO']}, {centro['C_POSTAL']}, {centro['D_LOCALIDAD']}, {centro['D_PROVINCIA']}"
                
                distancia = calcular_distancias(direccionOrigen, direccionDestino)
                centro["distancia"] = distancia.get("distancia en Km", "No disponible")
                centro["duracion"] = distancia.get("duracion", "No disponible")

            # Ordenar los centros por distancia
            centros.sort(key=lambda x: x.get("distancia", float("inf")))
        
        # Paginación
        totalCentros = len(centros)
        startIndex = (page - 1) * rowsPerPage
        endIndex = startIndex + rowsPerPage
        centrosPaginados = centros[startIndex:endIndex]

        print(f"Dirección de origen: {direccionOrigen}")
        print(f"Centros obtenidos: {len(centros)}")
        print(f"Página actual: {page}")
        print(f"Filas por Páginas: {rowsPerPage}")

        # Devuelve los centros obtenidos en un diccionario
        return {"centros": centrosPaginados, "total": totalCentros, "page": page, "rowsPerPage": rowsPerPage}
    except Exception as e:
        # Si ocurre una excepción, devuelve un mensaje de error y un código de estado 500
        return {"error": f"Error al obtener los centros: {str(e)}"}, 500


@router.get("/centros/tipos")
async def listar_tipos_de_centro():
    """
    Devuelve una lista de los tipos de centro únicos en la base de datos.
    """
    tipos = collection.distinct("D_DENOMINA")
    return {"tipos": tipos}


    




