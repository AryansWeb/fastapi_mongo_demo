# Usa una imagen oficial de Python como imagen base
FROM python:3.11-slim

# Establece el directorio de trabajo en el contenedor
WORKDIR /app

# Instala pipenv
RUN pip install pipenv

# Copia los archivos de dependencias
COPY Pipfile Pipfile.lock ./

# Instala las dependencias del proyecto
# --system instala los paquetes en el site-packages del sistema, ideal para contenedores
# --deploy se asegura de que Pipfile.lock esté actualizado y falla si no lo está
RUN pipenv install --system --deploy --ignore-pipfile

# Copia el resto del código de la aplicación
COPY . .

# Expone el puerto en el que se ejecuta la aplicación
EXPOSE 8000

# Define el comando para ejecutar la aplicación
# El --host 0.0.0.0 es crucial para que el servidor sea accesible desde fuera del contenedor
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
