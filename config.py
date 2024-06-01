import os

# Configuration Constants
MODELS_NAME_FOLDER = "models"
FQBN_ESP32 = "esp32:esp32:esp32"

# Get the current directory and calculate directories based on it
CWD = os.getcwd()
MODELS_DIRECTORY = os.path.join(CWD, MODELS_NAME_FOLDER)
