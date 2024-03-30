import os

# Constantes de configuración
MODELS_NAME_FOLDER = "models_to_deploy"
FQBN_ESP32 = "esp32:esp32:esp32"

# Obtener el directorio actual y calcular directorios basados en él
CWD = os.getcwd()
MODELS_DIRECTORY = os.path.join(CWD, MODELS_NAME_FOLDER)

