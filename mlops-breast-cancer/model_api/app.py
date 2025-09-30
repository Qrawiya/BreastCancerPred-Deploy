from flask import Flask, request, jsonify
import joblib
import pandas as pd
from pydantic import BaseModel, ValidationError
import logging
from logging.handlers import RotatingFileHandler
import os

app = Flask(__name__)

# ─────────────────────────────────────────────
# CONFIGURACIÓN DE LOGGING: archivo + consola
# ─────────────────────────────────────────────

if not os.path.exists("logs"):
    os.makedirs("logs")

log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Guardar logs con rotación (máx 5MB, 3 backups)
file_handler = RotatingFileHandler("logs/api.log", maxBytes=5_000_000, backupCount=3)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

# Mostrar logs en consola también
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(logging.INFO)

# Limpiar handlers previos para evitar duplicados
if app.logger.hasHandlers():
    app.logger.handlers.clear()

app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

# ─────────────────────────────────────────────
# CARGA DEL MODELO
# ─────────────────────────────────────────────

model = joblib.load('breast_cancer_model.pkl')


# ─────────────────────────────────────────────
# VALIDACIÓN DE ENTRADAS CON PYDANTIC
# ─────────────────────────────────────────────

class InputData(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float

# ─────────────────────────────────────────────
# RUTA GET /
# ─────────────────────────────────────────────
@app.route('/')
def home():
    """
    Ruta para comprobar que el servicio está activo.
    Retorna un mensaje JSON confirmando el estado de la API.
    """
    app.logger.info("GET / - Estado: API activa")
    return jsonify({"message": "API del modelo Breast Cancer está corriendo."})


# ─────────────────────────────────────────────
# RUTA POST /predict
# ─────────────────────────────────────────────
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)
        app.logger.info(f"POST /predict - Datos recibidos: {data}")

        # Validar datos con Pydantic
        validated_data = InputData(**data)

        # Convertir a DataFrame
        input_df = pd.DataFrame([validated_data.model_dump()])

        # Renombrar columnas con espacios (por compatibilidad con modelo)
        input_df.rename(columns={
            'concave_points_mean': 'concave points_mean',
            'concave_points_se': 'concave points_se',
            'concave_points_worst': 'concave points_worst'
        }, inplace=True)

        # Realizar predicción
        prediction = model.predict(input_df)[0]
        prediction_proba = model.predict_proba(input_df)[0]

        label_map = {0: "Benigno", 1: "Maligno"}

        response = {
            "prediction": int(prediction),
            "prediction_label": label_map[int(prediction)],
            "probability": prediction_proba.tolist()
        }

        app.logger.info(f"POST /predict - Respuesta enviada: {response}")
        return jsonify(response)

    except ValidationError as ve:
        app.logger.warning(f"POST /predict - Error de validación: {ve}")
        return jsonify({
            "error": "Datos inválidos",
            "details": ve.errors()
        }), 400

    except Exception as e:
        app.logger.error("POST /predict - Error inesperado", exc_info=True)
        return jsonify({"error": "Error interno del servidor"}), 500

# ─────────────────────────────────────────────
# EJECUCIÓN LOCAL / DOCKER
# ─────────────────────────────────────────────
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)
