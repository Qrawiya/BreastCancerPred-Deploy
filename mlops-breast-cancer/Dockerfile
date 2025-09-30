# Utiliza una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo requirements.txt y luego instalar las dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos de la API al contenedor
COPY model_api/ /app/

# Copiar el modelo desde la carpeta model (en la raíz)
COPY model/breast_cancer_model.pkl /app/model/

# Exponer el puerto que usará la API
EXPOSE 8001

# Comando para ejecutar la API cuando el contenedor se inicie
CMD ["python", "app.py"]
