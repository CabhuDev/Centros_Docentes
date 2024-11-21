# Manual Paso a Paso para Desplegar la Aplicación en Render

Este manual explica cómo desplegar tu aplicación web desarrollada con **FastAPI** en el backend y **HTML/CSS/JavaScript** en el frontend utilizando **Render**. Al final de este proceso, tu aplicación estará disponible en un dominio público de Render.

## Paso 1: Preparar la Aplicación para el Despliegue

1. **Requisitos Previos**
   - Asegúrate de tener una cuenta en [Render](https://render.com/).
   - Instala **Git** si aún no lo tienes ([descargar Git](https://git-scm.com/)).
   - Tener instalado **Python** y **Node.js** (para manejar dependencias del frontend).

2. **Estructura de Archivos**
   Asegúrate de que la estructura de archivos esté organizada como se describe previamente, con carpetas `backend` y `frontend`, y que todos los archivos requeridos estén presentes.

3. **Archivo `requirements.txt`**
   Asegúrate de que el archivo `requirements.txt` esté actualizado con todas las dependencias necesarias para la aplicación.
   
   Si necesitas generar el archivo `requirements.txt`, ejecuta el siguiente comando en la terminal:
   ```sh
   pip freeze > requirements.txt
   ```

4. **Archivo `start.sh`**
   Crea un archivo llamado `start.sh` en la raíz del proyecto. Este archivo le indica a Render cómo ejecutar tu aplicación.
   
   Contenido del `start.sh`:
   ```sh
   #!/bin/bash
   uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
   ```
   Asegúrate de dar permisos de ejecución al archivo:
   ```sh
   chmod +x start.sh
   ```

5. **Archivo `.env` para Variables de Entorno**
   Las variables de entorno, como las claves de la API de Google, deben configurarse directamente en Render y no en el archivo `.env` para mayor seguridad.

## Paso 2: Configurar el Proyecto para Render

1. **Subir el Proyecto a GitHub**
   Render requiere que el proyecto esté en un repositorio Git. Puedes subir tu proyecto a **GitHub**, **GitLab**, o cualquier otro repositorio Git:
   
   ```sh
   git init
   git add .
   git commit -m "Preparar proyecto para despliegue en Render"
   git remote add origin <URL_DEL_REPOSITORIO>
   git push -u origin master
   ```

2. **Crear un Nuevo Servicio en Render**
   - Ve a [Render.com](https://render.com/) e inicia sesión.
   - Haz clic en **"New"** y selecciona **"Web Service"**.
   - Conecta tu cuenta de **GitHub** o **GitLab** a Render y selecciona el repositorio donde subiste tu proyecto.

3. **Configurar el Servicio**
   Al configurar tu servicio web, Render te pedirá cierta información:
   - **Name**: Dale un nombre a tu aplicación.
   - **Branch**: Selecciona la rama de tu repositorio (normalmente `master` o `main`).
   - **Build Command**: Si usas solo Python, Render lo detectará automáticamente. Sin embargo, puedes especificar:
     ```sh
     pip install -r requirements.txt
     ```
   - **Start Command**: Indica a Render cómo iniciar la aplicación. Usa el script de inicio que creaste:
     ```sh
     ./start.sh
     ```
   - **Environment**: Selecciona **Python 3**.

4. **Configurar Variables de Entorno**
   Configura las variables de entorno necesarias (como claves de API) en el panel de Render.
   - Ve a **Settings** > **Environment** > **Add Environment Variable** y añade las variables necesarias como `GOOGLE_API_KEY`, `DATABASE_URL`, etc.

## Paso 3: Desplegar la Aplicación en Render

1. **Deploy**
   Render comenzará el despliegue automáticamente cuando crees el servicio. Puedes ver el progreso en la pestaña de **Logs**.

2. **Verificar el Despliegue**
   Cuando el despliegue sea exitoso, Render te proporcionará una URL pública para acceder a tu aplicación. Haz clic en el enlace proporcionado para verificar si la aplicación está funcionando correctamente.

## Paso 4: Solucionar Problemas Comunes

1. **Logs de Render**
   Si la aplicación no se despliega correctamente, puedes ver los registros de Render para diagnosticar problemas en la sección de **Logs** del servicio.

2. **Problemas con Archivos Estáticos**
   Asegúrate de que todos los archivos estáticos (imágenes, CSS, JavaScript) estén en la carpeta correcta y sean accesibles desde el servidor. Puedes usar servicios externos como **Cloudinary** o **AWS S3** si los archivos son demasiado grandes.

3. **Códigos de Error Comunes**
   - **Error 502**: Esto indica que la aplicación no pudo iniciar correctamente. Verifica que los comandos de inicio (`start.sh`) y las configuraciones sean correctas.
   - **Permiso Denegado**: Asegúrate de que el archivo `start.sh` tenga permisos de ejecución (`chmod +x start.sh`).

## Paso 5: Consideraciones para Producción

1. **Escalabilidad**
   Render escala automáticamente según la demanda. Si notas un aumento en el tráfico, Render ajustará la cantidad de recursos utilizados automáticamente.

2. **SSL/TLS (HTTPS)**
   Render proporciona automáticamente SSL gratuito para aplicaciones bajo el dominio render.com y para dominios personalizados.

3. **Dominios Personalizados**
   Puedes añadir tu propio dominio personalizado en la sección **Settings** del servicio y configurar el DNS según las instrucciones de Render.

## Paso 6: Desplegar Actualizaciones

Cada vez que realices cambios en tu proyecto y los subas al repositorio, Render desplegará automáticamente los nuevos cambios. Asegúrate de hacer `commit` y `push` de tus cambios:

```sh
git add .
git commit -m "Actualizar aplicación"
git push origin master
```

Render detectará automáticamente los cambios y actualizará la aplicación.

## Resumen
Este manual cubre el proceso de despliegue de tu aplicación **FastAPI** con **HTML/CSS/JavaScript** en **Render**, desde la preparación del proyecto hasta el despliegue y configuración de producción. Con estos pasos, podrás tener tu aplicación accesible públicamente y en funcionamiento en un dominio de Render.

