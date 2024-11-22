# Centros Educativos de Andalucía

## Descripción General del Proyecto

Este proyecto permite visualizar información sobre centros educativos de Andalucía y aplicar filtros de forma interactiva. Utiliza una interfaz de usuario intuitiva para mostrar información relevante, como la localidad, provincia, y el tipo de centro, ofreciendo al usuario la capacidad de filtrar los datos de forma dinámica, similar a una hoja de cálculo tipo Excel. Además, el proyecto hace uso de la API de Google Maps para calcular distancias y tiempos de viaje a los diferentes centros, añadiendo así una capa adicional de información para la toma de decisiones.

La aplicación está compuesta por un backend desarrollado en **FastAPI** que gestiona la lógica de negocio y sirve los datos desde varios archivos CSV, mientras que el frontend está construido con **HTML**, **CSS** y **JavaScript**, proporcionando una experiencia interactiva para el usuario.

## Tecnologías Utilizadas

- **Backend**: FastAPI, Python, CSV, Google Maps API
- **Frontend**: HTML5, CSS3, JavaScript
- **Otras Herramientas**: Uvicorn (para correr el servidor FastAPI), dotenv (para gestionar variables de entorno)

## Estructura del Proyecto

```
/CentrosJuntaAndalucia/v3.0
│
├── backend/                          # Contiene la lógica y servicios del lado del servidor
│   ├── app/
│   │   ├── __init__.py               # Inicialización del módulo app (configuración general)
│   │   ├── main.py                   # Punto de entrada para iniciar la aplicación FastAPI/
│   │   ├── models/                   # Define los modelos de datos (esquemas)
│   │   │   ├── centro.py             # Clase CentroEducativo y otros modelos necesarios
│   │   │   └── __init__.py           
│   │   ├── routers/                  # Define las rutas (endpoints) de la API
│   │   │   ├── api_routes.py         # Rutas para manejar CRUD de datos CSV
│   │   │   └── __init__.py
│   │   ├── services/                 # Servicios y lógica de negocio
│   │   │   ├── csv_service.py        # Funciones de gestión de los archivos CSV (leer, añadir, modificar, eliminar)
│   │   │   ├── googleCoonect.py      # Funciones para conectarse con la API de Google
│   │   │   ├── csvToMongo.py         # Lógica para pasar el cvs de datos a MongoDB
│   │   │   ├── consultasMongo.py     # Lógica para realizar consultas a MongoDB
│   │   │   └── __init__.py
│   │   ├── utils/                    # Utilidades generales que pueden ser compartidas
│   │   │   ├── helpers.py            # Funciones auxiliares que se usan en múltiples partes del proyecto
│   │   │   └── __init__.py
│   │   └── config.py                 # Configuraciones generales (por ejemplo, claves de API)
│   └── venv/                         # Entorno virtual para las dependencias de Python
│
├── data/                             # Archivos CSV (datos)
│   ├── centros_compensatoria.csv     # Diferentes tipos de centros educativos
│   ├── centros_dificil.csv
│   ├── centros_educativos_ordenados.csv
│   ├── centros_exportados.csv
│   ├── centros_todos.csv
│   └── coincidencias.csv
│
├── frontend/                         # Parte de la interfaz de usuario
│   ├── index.html                    # Página principal HTML
│   ├── css/                          # Archivos de estilos CSS
│   │   └── style.css                 # Estilo de la aplicación web
│   ├── js/                           # Archivos JavaScript para interacción del usuario
│   │   ├── main.js                   # Archivo principal que importa todas las funciones y llama a inicializarTabla()
│   │   config.js                 # Contendrá configuraciones globales y constantes
│   │   NoRealizado├── filterService.js          # Contendrá toda la lógica relacionada con el filtrado de los datos
│   │   NoRealizado├── uiService.js              # Contendrá todas las funciones que manejan la manipulación del DOM y la visualización
│   │   └── apiService.js             # Encargado de la interacción con la API
│   └── assets/                       # Recursos estáticos adicionales
│       ├── images/                   # Imágenes utilizadas en la interfaz
│       └── fonts/                    # Fuentes si son necesarias
│
├── .env                              # Variables de entorno (por ejemplo, claves de API)
├── .gitignore                        # Ignorar archivos innecesarios en Git (por ejemplo, venv, .env, archivos temporales)
├── LICENSE                           # Licencia del proyecto
├── README.md                         # Documentación sobre cómo configurar y usar la aplicación
└── requirements.txt                  # Lista de dependencias de Python necesarias para ejecutar el proyecto
```

## Instrucciones de Instalación

1. **Clonar el Repositorio**

   ```sh
   git clone https://github.com/CabhuDev/Centros_Docentes.git
   cd CentrosJuntaAndalucia
   ```

2. **Crear y Activar un Entorno Virtual**

   - En **Windows**:
     ```sh
     python -m venv venv
     venv\Scripts\activate
     ```
   - En **Linux/MacOS**:
     ```sh
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Instalar las Dependencias**

   ```sh
   pip install -r requirements.txt
   ```

4. **Configurar Variables de Entorno**

   - Crea un archivo `.env` en la raíz del proyecto para almacenar las claves de la API de Google Maps y otras configuraciones necesarias. Por ejemplo:
     ```
     GOOGLE_API_KEY=tu_clave_api
     ```

5. **Ejecutar el Servidor**

   ```sh
   uvicorn backend.app.main:app --reload
   ```

   Esto iniciará el servidor en `http://localhost:8000`.

## Uso del Proyecto

- **Acceder a la Aplicación**: Abre `index.html` en un navegador para acceder a la interfaz de usuario.
- **Filtrar los Datos**: Utiliza los filtros en la cabecera de la tabla para buscar centros educativos específicos por municipio, provincia, tipo, etc.
- **Calcular Distancias**: Puedes calcular la distancia y el tiempo de viaje a un centro educativo utilizando la API de Google Maps.

## Contribución

Este proyecto está abierto a contribuciones. Si deseas contribuir, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva_funcionalidad`).
3. Haz commit de tus cambios (`git commit -m 'Añadir nueva funcionalidad'`).
4. Empuja tu rama (`git push origin feature/nueva_funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## Autor

Proyecto desarrollado por [Tu Nombre]. Puedes contactar conmigo en pablo.cabello.hurtado@gmail.com.

