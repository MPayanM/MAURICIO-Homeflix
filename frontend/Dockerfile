# Usamos una imagen base de Python oficial con Python 3.11
FROM python:3.11-slim

# Definir el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de dependencias (requirements.txt)
COPY requirements.txt .

# Instalar las dependencias del archivo requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que Streamlit va a correr (8501 por defecto)
EXPOSE 8501

# Comando para iniciar la aplicación Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
