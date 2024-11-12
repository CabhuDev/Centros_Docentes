
from models.CentroEducativo import CentroEducativo

import csv 
import pandas as pd
import re


def cargar_csv_centros(csv_cargado,direccion_origen):
    """
    Carga y procesa los datos de centros educativos desde un archivo CSV.
    Esta función lee un archivo CSV que contiene información sobre centros educativos,
    crea objetos CentroEducativo para cada registro, calcula la distancia desde una
    dirección de origen y devuelve una lista ordenada por duración del trayecto.
    Args:
        csv_cargado (str): Ruta al archivo CSV que contiene los datos de los centros educativos.
                        El CSV debe contener las columnas: D_DOMICILIO, C_POSTAL, D_MUNICIPIO,
                        D_PROVINCIA, D_DENOMINA, D_ESPECIFICA, codigo, D_TIPO
        list: Lista ordenada de objetos CentroEducativo, ordenados por la duración del
              trayecto desde la dirección de origen. Los centros para los que no se pudo
              calcular la distancia se excluyen del resultado.
    Requires:
        - Clase CentroEducativo con método calcula_distancia_clase()
        - Variable global direccion_origen definida
        - Módulo csv importado
    Example:
        >>> centros = cargar_csv_centros('ruta/al/archivo.csv')
        >>> for centro in centros:
        >>>     print(f"{centro.nombre_centro}: {centro.duracion}")
    """
    
    # Lista para almacenar los objetos de tipo CentroEducativo
    centros_educativos_completo = []

    # Leer el archivo CSV y crear objetos de tipo CentroEducativo
    with open(csv_cargado, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            centro = CentroEducativo(
                direccion=row["D_DOMICILIO"],
                codigo_postal = row["C_POSTAL"],
                municipio=row["D_MUNICIPIO"],
                provincia=row["D_PROVINCIA"],
                tipo_centro=row["D_DENOMINA"],
                nombre_centro=row["D_ESPECIFICA"],
                codigo_centro = row["codigo"],
                publico_privado = row["D_TIPO"],
                bil = "Empty",
                compensatoria="Empty"
            )

            # Calcular la distancia desde la dirección de origen
            if centro.calcula_distancia_clase(direccion_origen):
                centros_educativos_completo.append(centro)

    return centros_educativos_completo


def ordenar_centros_duracion(centros_educativos_completo):
    """
    Ordena los centros educativos por duración estimada de viaje.
    Args:
        centros_educativos_completo (list): Lista de objetos CentroEducativo
    Returns:
        list: Lista de objetos CentroEducativo ordenados por duración
    """
    # Ordenar los centros por duración estimada (convertida a minutos)
    centros_educativos_ordenados = sorted(centros_educativos_completo, key=lambda x: CentroEducativo.convertir_duracion_a_minutos(x.duracion) if x.duracion is not None else float('inf'))
    return centros_educativos_ordenados



def exportar_csv_centros(nombre_csv_exportar,csv_cargado):
    """
    Exporta una lista de centros educativos a un archivo CSV.
    Esta función toma los datos de centros educativos cargados previamente y los exporta
    a un nuevo archivo CSV con un formato específico incluyendo información detallada
    de cada centro.
    Args:
        nombre_csv_exportar (str): Ruta del archivo CSV donde se exportarán los datos.
    Returns:
        None
    Example:
        >>> exportar_csv_centros("ruta/archivo_exportado.csv")
    Notes:
        - El archivo CSV se crea con codificación UTF-8
        - Los campos incluidos son:
            * Dirección
            * Código Postal
            * Municipio
            * Provincia
            * Tipo Centro
            * Nombre Centro
            * Código Centro
            * Público/Privado
            * Idiomas
            * Distancia (Km)
            * Duración
    """

    # Definir los encabezados para el nuevo CSV
    headers = ["Dirección", "Código Postal", "Municipio", "Provincia", "Tipo Centro", "Nombre Centro", "Código Centro", "Público/Privado", "Idiomas", "Distancia (Km)", "Duración","Centro Compensatorio"]

    # Exportar la lista de objetos CentroEducativo a un nuevo CSV
    with open(nombre_csv_exportar, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        
        for centro in csv_cargado:
            writer.writerow({
                "Código Centro": centro.codigo_centro,
                "Tipo Centro": centro.tipo_centro,
                "Nombre Centro": centro.nombre_centro,
                "Público/Privado": centro.publico_privado,
                "Dirección": centro.direccion,
                "Código Postal": centro.codigo_postal,
                "Municipio": centro.municipio,
                "Provincia": centro.provincia,
                "Distancia (Km)": centro.distancia_km,
                "Duración": centro.duracion,
                "Idiomas": centro.bil,
                "Centro Compensatorio": centro.compensatoria
            })


def coincidencias(csv1, csv2):
    """
    Compara dos archivos CSV y encuentra registros coincidentes por código de centro.
    
    Args:
        csv1 (str): Ruta al primer CSV (iso-8859-1, delimitador ';')
        csv2 (str): Ruta al segundo CSV (utf-8)
    """
    # Diccionario para almacenar datos del primer CSV
    datos_csv1 = {}

    # Leer primer CSV (utf-8)
    with open(csv2, mode='r', encoding='utf-8') as file1:
        reader1 = csv.DictReader(file1)   
        for row in reader1:
            # Limpiar y extraer código numérico del centro
            codigo_centro = row['codigo'].strip()
            # Usar regex para extraer solo dígitos del código
            match = re.search(r'\d+', codigo_centro)
            # Si hay coincidencia usar dígitos, sino código completo
            codigo_numerico = match.group() if match else codigo_centro
            datos_csv1[codigo_numerico] = row

    # Debug: mostrar códigos encontrados
    print(datos_csv1.keys())

    # Lista para almacenar datos del segundo CSV
    datos_csv2 = []

    # Leer segundo CSV (iso-8859-1)
    with open(csv1, mode='r', encoding='iso-8859-1') as file2:
        reader2 = csv.DictReader(file2, delimiter=';')
        for row in reader2:
            datos_csv2.append(row)

    # Lista para almacenar coincidencias encontradas
    coincidencias = []

    # Buscar coincidencias entre ambos CSVs
    for row in datos_csv2:
        codigo_centro = row["codigo"].strip()
        # Si el código existe en el primer CSV, guardar coincidencia
        if codigo_centro in datos_csv1:
            coincidencias.append(row)

    # Obtener headers del primer registro para el CSV de salida
    headers = datos_csv2[0].keys()

    # Crear nuevo CSV con las coincidencias encontradas
    with open('coincidencias.csv', mode='w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=headers)
        writer.writeheader()  # Escribir headers
        writer.writerows(coincidencias)  # Escribir coincidencias

    print("Se han encontrado y exportado las coincidencias en 'coincidencias.csv'.")
    

def cotejar_compensatorios(nombre_csv_exportar,csv_compensatorios):
    # Leer el primer CSV y almacenar sus registros en un diccionario utilizando "codigo_centro" como clave
    datos_csv1 = {}

    with open(nombre_csv_exportar, mode='r', encoding='utf-8') as file1:
        reader1 = csv.DictReader(file1)   
        for row in reader1:
            # Almacenar cada fila usando el "codigo_centro" como clave
            codigo_centro = row['Código Centro'].strip()
            match = re.search(r'\d+', codigo_centro)
            codigo_numerico = match.group() if match else codigo_centro  # Extraer solo los dígitos si hay coincidencia
            datos_csv1[codigo_numerico] = row

    # Leer el segundo CSV y almacenar en una lista los registros
    datos_csv2 = []

    with open(csv_compensatorios, mode='r', encoding='utf-8') as file2:
        reader2 = csv.DictReader(file2)
        for row in reader2:
            datos_csv2.append(row)


    # Crear una lista para almacenar los registros coincidentes
    coincidencias_compensatorios = []
    # Actualizar el valor bil en datos_csv1 cuando hay coincidencia
    for row in datos_csv2:
        codigo_centro = row["Código Centro"].strip()
        if codigo_centro in datos_csv1:
            datos_csv1[codigo_centro]["Centro Compensatorio"] = "Es compensatorio"
            coincidencias_compensatorios.append(row)

    # Escribir los datos actualizados al CSV
    headers = datos_csv1[next(iter(datos_csv1))].keys()  # Get headers from first item
    with open(nombre_csv_exportar, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in datos_csv1.values():
            writer.writerow(row)


    print("Se han encontrado y exportado las coincidencias en 'coincidencias.csv'.")



def cotejar_bilingues(nombre_csv_exportar,csv_bilingues):
    """
    Coteja los centros bilingües de un archivo CSV con los centros de otro archivo CSV.
    Esta función toma dos archivos CSV, uno con centros educativos y otro con centros bilingües,
    y actualiza el campo 'Idiomas' en el primer archivo si un centro es bilingüe.
    Args:
        csv_coincidencias (str): Ruta al archivo CSV con los centros educativos (codificación utf-8)
        csv_bilingues (str): Ruta al archivo CSV con los centros bilingües (codificación iso-8859-1, delimitador ';')
    Returns:
        None. Actualiza el archivo 'csv_coincidencias' con los centros bilingües.
    Notas:
        - El archivo 'csv_coincidencias' se actualiza con el campo 'Idiomas' si un centro es bilingüe.
        - Ambos archivos deben tener una columna llamada 'codigo' para cotejar los centros.
    Ejemplo:
        cotejar_bilingues('centros.csv', 'centros_bilingues.csv')
    """
    # Leer el primer CSV y almacenar sus registros en un diccionario utilizando "codigo_centro" como clave
    datos_csv1 = {}

    with open(nombre_csv_exportar, mode='r', encoding='utf-8') as file1:
        reader1 = csv.DictReader(file1)   
        for row in reader1:
            # Almacenar cada fila usando el "codigo_centro" como clave
            codigo_centro = row['Código Centro'].strip()
            match = re.search(r'\d+', codigo_centro)
            codigo_numerico = match.group() if match else codigo_centro  # Extraer solo los dígitos si hay coincidencia
            datos_csv1[codigo_numerico] = row

    # Leer el segundo CSV y almacenar en una lista los registros
    datos_csv2 = []

    with open(csv_bilingues, mode='r', encoding='iso-8859-1') as file2:
        reader2 = csv.DictReader(file2,delimiter=';')
        for row in reader2:
            datos_csv2.append(row)


    # Crear una lista para almacenar los registros coincidentes
    coincidencias_bilingues = []
    # Actualizar el valor bil en datos_csv1 cuando hay coincidencia
    for row in datos_csv2:
        codigo_centro = row["codigo"].strip()
        if codigo_centro in datos_csv1:
            datos_csv1[codigo_centro]["Idiomas"] = "Es bilingüe"
            coincidencias_bilingues.append(row)

    # Escribir los datos actualizados al CSV
    headers = datos_csv1[next(iter(datos_csv1))].keys()  # Get headers from first item
    with open(nombre_csv_exportar, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in datos_csv1.values():
            writer.writerow(row)


    print("Se han encontrado y exportado las coincidencias en 'coincidencias.csv'.")


