#!/bin/bash
set -euo pipefail

IMAGE_NAME="breast-cancer-api"
CONTAINER_NAME="breast-cancer-api-container"
HOST_PORT=8001
CONTAINER_PORT=8001
BASE_URL="http://localhost:$HOST_PORT"

echo "Verificando archivos esenciales..."
for file in Dockerfile requirements.txt model_api/app.py model/breast_cancer_model.pkl; do
  if [ ! -f "$file" ]; then
    echo "❌ ERROR: No se encontró el archivo $file"
    exit 1
  fi
done

command -v docker >/dev/null 2>&1 || { echo >&2 "❌ Docker no está instalado o no está en PATH."; exit 1; }

# Detener y eliminar contenedor si existe
if [ "$(docker ps -q -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "El contenedor $CONTAINER_NAME ya está corriendo. Deteniéndolo..."
  docker stop $CONTAINER_NAME
  echo "Eliminando contenedor $CONTAINER_NAME..."
  docker rm $CONTAINER_NAME
fi

if [ "$(docker ps -aq -f status=exited -f name=^/${CONTAINER_NAME}$)" ]; then
  echo "Eliminando contenedor detenido $CONTAINER_NAME..."
  docker rm $CONTAINER_NAME
fi

echo "Construyendo imagen Docker..."
docker build -t $IMAGE_NAME .

echo "Ejecutando contenedor..."
docker run -d -p $HOST_PORT:$CONTAINER_PORT --name $CONTAINER_NAME $IMAGE_NAME

echo "Esperando a que la API arranque..."
MAX_RETRIES=10
for i in $(seq 1 $MAX_RETRIES); do
  HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/")
  if [ "$HTTP_STATUS" = "200" ]; then
    echo "✅ API está corriendo correctamente en $BASE_URL/"
    break
  else
    echo "Intento $i/$MAX_RETRIES: API aún no responde (status: $HTTP_STATUS), reintentando en 2s..."
    sleep 2
  fi

  if [ "$i" -eq "$MAX_RETRIES" ]; then
    echo "❌ No se pudo conectar a la API en $BASE_URL/ después de $MAX_RETRIES intentos."
    echo "Mostrando últimos 20 logs del contenedor para debug:"
    docker logs --tail 20 $CONTAINER_NAME
    exit 1
  fi
done

echo "Mostrando últimos 20 logs del contenedor:"
docker logs --tail 20 $CONTAINER_NAME

echo "Limpiando contenedores detenidos huérfanos..."
docker container prune -f

echo "Limpiando imágenes dangling (sin tag)..."
docker image prune -f

echo "Proceso finalizado."
