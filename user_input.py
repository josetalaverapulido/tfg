# Variables inicializadas, listas para ser actualizadas con la entrada del usuario
from config import MODELS_DIRECTORY
import os

# Variables inicializadas
file_name = ""
file_directory = ""
ssid = ""
password = ""
ip_esp32 = ""
mqtt_client_name = ""
mqtt_server = ""
mqtt_port = ""
receive_topic = ""
send_topic = ""



# Función para actualizar file_directory
def set_file_name(new_value):
    global file_name
    file_name = new_value
    
# Función para actualizar file_name
def set_file_directory(new_value):
    global file_directory
    file_directory = os.path.join(MODELS_DIRECTORY, new_value)
    print('file_directory ', file_directory)


# Función para actualizar ssid
def set_ssid(new_value):
    global ssid
    ssid = new_value

# Función para actualizar password
def set_password(new_value):
    global password
    password = new_value

# Función para actualizar ip_esp32
def set_ip_esp32(new_value):
    global ip_esp32
    ip_esp32 = new_value

# Función para actualizar mqtt_client_name
def set_mqtt_client_name(new_value):
    global mqtt_client_name
    mqtt_client_name = new_value

# Función para actualizar mqtt_server
def set_mqtt_server(new_value):
    global mqtt_server
    mqtt_server = new_value

# Función para actualizar mqtt_port
def set_mqtt_port(new_value):
    global mqtt_port
    mqtt_port = new_value

# Función para actualizar receive_topic
def set_receive_topic(new_value):
    global receive_topic
    receive_topic = new_value

# Función para actualizar send_topic
def set_send_topic(new_value):
    global send_topic
    send_topic = new_value


# Función para obtener file_name
def get_file_name():
    return file_name

# Función para obtener file_directory
def get_file_directory():
    return file_directory

# Función para obtener ssid
def get_ssid():
    return ssid

# Función para obtener password
def get_password():
    return password

# Función para obtener ip_esp32
def get_ip_esp32():
    return ip_esp32

# Función para obtener mqtt_client_name
def get_mqtt_client_name():
    return mqtt_client_name

# Función para obtener mqtt_server
def get_mqtt_server():
    return mqtt_server

# Función para obtener mqtt_port
def get_mqtt_port():
    return mqtt_port

# Función para obtener receive_topic
def get_receive_topic():
    return receive_topic

# Función para obtener send_topic
def get_send_topic():
    return send_topic