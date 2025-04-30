# Usamos una imagen base de Python
FROM python:3.11-slim

# Instalamos las dependencias del sistema necesarias
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    make \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecemos el directorio de trabajo
WORKDIR /app

# Copiamos el archivo de dependencias (requirements.txt) al contenedor
COPY requirements.txt /app/requirements.txt

# Instalamos las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copiamos todo el código fuente del backend al contenedor
COPY . /app

# Exponemos el puerto 8000 para FastAPI
EXPOSE 8000

# Comando para ejecutar la aplicación con Uvicorn
CMD ["uvicorn", "mainv2:app", "--host", "0.0.0.0", "--port", "8000"]