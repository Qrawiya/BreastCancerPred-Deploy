# Proyecto de Predicción de Cáncer de Mama

Este proyecto tiene como objetivo desarrollar una API REST utilizando Flask para predecir si un tumor es benigno o maligno utilizando el conjunto de datos de cáncer de mama de Wisconsin. Se implementan varias herramientas y técnicas para facilitar el desarrollo, pruebas, despliegue y gestión del modelo.

## Estructura del Proyecto

mlops-breast-cancer/
│
├── model_api/ # Carpeta con la API Flask
│ ├── app.py # Código de la API en Flask
│ ├── Dockerfile # Dockerfile para la contenedorización de la API
│ ├── requirements.txt # Dependencias del proyecto
│ ├── logs/ # Carpeta de logs (api.log)
│ └── init.py
│
├── model/ # Carpeta que contiene el modelo entrenado
│ └── breast_cancer_model.pkl # Modelo serializado con joblib
│
├── data/ # Carpeta con el dataset original
│ └── breast_cancer_data.csv # Dataset de cáncer de mama de Wisconsin
│
├── notebooks/ # Jupyter notebooks para exploraciones y entrenamiento
│ ├── EDA_data.ipynb # Notebook con el análisis exploratorio de datos
│ └── Train_model.ipynb # Notebook con el entrenamiento del modelo
│
├── tests/ # Carpeta con los tests de la API
│ └── test_api.py # Pruebas automatizadas de la API
│
└── README.md # Este archivo


## Descripción

La API creada en Flask permite predecir si un tumor en una mamografía es benigno o maligno usando un modelo de clasificación entrenado con el conjunto de datos de cáncer de mama de Wisconsin. La API expone dos rutas:

- **GET /**: Devuelve un mensaje de estado indicando que la API está activa.
- **POST /predict**: Recibe un conjunto de características del tumor y devuelve la predicción del modelo, indicando si es benigno o maligno.

### Validación de Entradas

La entrada al endpoint `POST /predict` está validada utilizando **Pydantic**. Si los datos no son válidos, se devolverá un error con detalles sobre los campos faltantes o con formato incorrecto.

### Logging

El proyecto incluye un sistema de logging tanto en consola como en un archivo (`api.log`) para registrar todas las solicitudes y errores importantes. Los logs se gestionan con rotación para evitar que los archivos se vuelvan demasiado grandes.

### Dockerización

El proyecto está dockerizado para facilitar su implementación en cualquier entorno. El archivo `Dockerfile` incluye todos los pasos necesarios para crear una imagen con el entorno necesario para ejecutar la API.

## Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/tuusuario/mlops-breast-cancer.git
cd mlops-breast-cancer

2. **Instala las dependencias:**

Asegúrate de tener Docker y Python instalados.

Instalar dependencias con pip:

pip install -r model_api/requirements.txt


3. **Ejecuta la API en Flask:**

cd model_api
python app.py

4. **Dockerización**

Si prefieres ejecutar la API en un contenedor Docker, construye la imagen y ejecuta el contenedor:

docker build -t breast-cancer-api .
docker run -p 8001:8001 breast-cancer-api

La API estará disponible en http://127.0.0.1:8001.

** Pruebas **

Para probar la API, se incluyen pruebas automatizadas en el archivo test_api.py dentro de la carpeta tests/. Este archivo realiza pruebas de las rutas GET / y POST /predict.

Para ejecutar los tests, utiliza el siguiente comando:

python tests/test_api.py


**Detalles de las pruebas**

GET /: Verifica que la API esté activa y responda con el mensaje esperado.

POST /predict (válido): Envía un conjunto válido de datos y comprueba que la predicción sea correcta.

POST /predict (campo faltante): Envía una solicitud con campos faltantes y comprueba que la API devuelva un error adecuado.

POST /predict (JSON inválido): Envía datos con formato incorrecto (como texto en un campo numérico) y verifica que la API devuelva un error adecuado.

**Consideraciones**

El modelo de predicción se entrena utilizando scikit-learn y se serializa en un archivo .pkl con joblib.

El conjunto de datos utilizado es el Breast Cancer Wisconsin dataset, que está disponible públicamente en Kaggle.

El uso de Docker permite empaquetar la API y sus dependencias para facilitar su despliegue en cualquier entorno.

**Tecnologías**

Flask: Para crear la API REST.

Pandas y scikit-learn: Para procesar y entrenar el modelo de machine learning.

Pydantic: Para la validación de entradas.

Docker: Para contenedorización.

Joblib: Para la serialización del modelo entrenado.

Logging: Para el manejo de logs.

**Contribuciones**

Las contribuciones son bienvenidas. Si deseas contribuir al proyecto, por favor abre un pull request con tus cambios.

Autor

Nombre: [Cristobal Araya]

Correo: [araya.cristo@gmail.com]

GitHub: [https://github.com/Qrawiya]
