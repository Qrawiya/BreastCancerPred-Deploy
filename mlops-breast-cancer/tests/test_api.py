import requests
import json
from colorama import init, Fore, Style

# Inicializar colorama
init(autoreset=True)

url = "http://127.0.0.1:8001"  # Puerto actualizado a 8001

def print_section(title):
    print(Fore.YELLOW + f"\n======== Test: {title} ========" + Style.RESET_ALL)

def test_home():
    print_section("GET /")
    response = requests.get(url + "/")
    print("Status code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    assert response.status_code == 200
    data = response.json()
    assert data.get("message") == "API del modelo Breast Cancer está corriendo."
    print(Fore.GREEN + "✅ test_home passed!\n")

def test_predict():
    print_section("POST /predict (válido)")
    data = {
        "radius_mean": 14.0,
        "texture_mean": 20.0,
        "perimeter_mean": 90.0,
        "area_mean": 600.0,
        "smoothness_mean": 0.1,
        "compactness_mean": 0.2,
        "concavity_mean": 0.1,
        "concave_points_mean": 0.05,
        "symmetry_mean": 0.2,
        "fractal_dimension_mean": 0.06,
        "radius_se": 0.5,
        "texture_se": 1.0,
        "perimeter_se": 3.0,
        "area_se": 40.0,
        "smoothness_se": 0.01,
        "compactness_se": 0.02,
        "concavity_se": 0.01,
        "concave_points_se": 0.005,
        "symmetry_se": 0.02,
        "fractal_dimension_se": 0.003,
        "radius_worst": 16.0,
        "texture_worst": 25.0,
        "perimeter_worst": 100.0,
        "area_worst": 700.0,
        "smoothness_worst": 0.15,
        "compactness_worst": 0.3,
        "concavity_worst": 0.2,
        "concave_points_worst": 0.1,
        "symmetry_worst": 0.3,
        "fractal_dimension_worst": 0.07
    }
    response = requests.post(url + "/predict", json=data)
    print("Status code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2))
    assert response.status_code == 200
    result = response.json()
    assert "prediction" in result
    assert "prediction_label" in result
    assert "probability" in result
    print(Fore.GREEN + "✅ test_predict passed!\n")

def test_predict_missing_field():
    print_section("POST /predict (campo faltante)")
    data = {
        # Falta 'texture_mean'
        "radius_mean": 14.0,
        "perimeter_mean": 90.0,
        "area_mean": 600.0,
        "smoothness_mean": 0.1,
        "compactness_mean": 0.2,
        "concavity_mean": 0.1,
        "concave_points_mean": 0.05,
        "symmetry_mean": 0.2,
        "fractal_dimension_mean": 0.06,
        "radius_se": 0.5,
        "texture_se": 1.0,
        "perimeter_se": 3.0,
        "area_se": 40.0,
        "smoothness_se": 0.01,
        "compactness_se": 0.02,
        "concavity_se": 0.01,
        "concave_points_se": 0.005,
        "symmetry_se": 0.02,
        "fractal_dimension_se": 0.003,
        "radius_worst": 16.0,
        "texture_worst": 25.0,
        "perimeter_worst": 100.0,
        "area_worst": 700.0,
        "smoothness_worst": 0.15,
        "compactness_worst": 0.3,
        "concavity_worst": 0.2,
        "concave_points_worst": 0.1,
        "symmetry_worst": 0.3,
        "fractal_dimension_worst": 0.07
    }
    response = requests.post(url + "/predict", json=data)
    print("Status code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    assert response.status_code == 400
    print(Fore.GREEN + "✅ test_predict_missing_field passed!\n")

def test_predict_invalid_json():
    print_section("POST /predict (JSON inválido)")
    data = {
        "radius_mean": "no_es_numero",  # Valor inválido
        "texture_mean": 20.0,
        "perimeter_mean": 90.0,
        "area_mean": 600.0,
        "smoothness_mean": 0.1,
        "compactness_mean": 0.2,
        "concavity_mean": 0.1,
        "concave_points_mean": 0.05,
        "symmetry_mean": 0.2,
        "fractal_dimension_mean": 0.06,
        "radius_se": 0.5,
        "texture_se": 1.0,
        "perimeter_se": 3.0,
        "area_se": 40.0,
        "smoothness_se": 0.01,
        "compactness_se": 0.02,
        "concavity_se": 0.01,
        "concave_points_se": 0.005,
        "symmetry_se": 0.02,
        "fractal_dimension_se": 0.003,
        "radius_worst": 16.0,
        "texture_worst": 25.0,
        "perimeter_worst": 100.0,
        "area_worst": 700.0,
        "smoothness_worst": 0.15,
        "compactness_worst": 0.3,
        "concavity_worst": 0.2,
        "concave_points_worst": 0.1,
        "symmetry_worst": 0.3,
        "fractal_dimension_worst": 0.07
    }
    response = requests.post(url + "/predict", json=data)
    print("Status code:", response.status_code)
    print("Response JSON:")
    print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    assert response.status_code == 400
    print(Fore.GREEN + "✅ test_predict_invalid_json passed!\n")

if __name__ == "__main__":
    try:
        test_home()
    except Exception as e:
        print(Fore.RED + f"❌ test_home failed: {e}\n")

    try:
        test_predict()
    except Exception as e:
        print(Fore.RED + f"❌ test_predict failed: {e}\n")

    try:
        test_predict_missing_field()
    except Exception as e:
        print(Fore.RED + f"❌ test_predict_missing_field failed: {e}\n")

    try:
        test_predict_invalid_json()
    except Exception as e:
        print(Fore.RED + f"❌ test_predict_invalid_json failed: {e}\n")
