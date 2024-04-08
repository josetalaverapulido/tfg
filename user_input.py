from config import MODELS_DIRECTORY
import os

# Initialize variables
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
device_port = ""



def set_file_name(new_value):
    global file_name
    file_name = new_value
    
def set_file_directory(new_value):
    global file_directory
    file_directory = os.path.join(MODELS_DIRECTORY, new_value)
    print('file_directory ', file_directory)


def set_ssid(new_value):
    global ssid
    ssid = new_value

def set_password(new_value):
    global password
    password = new_value

def set_ip_esp32(new_value):
    global ip_esp32
    ip_esp32 = new_value

def set_mqtt_client_name(new_value):
    global mqtt_client_name
    mqtt_client_name = new_value

def set_mqtt_server(new_value):
    global mqtt_server
    mqtt_server = new_value

def set_mqtt_port(new_value):
    global mqtt_port
    mqtt_port = new_value

def set_receive_topic(new_value):
    global receive_topic
    receive_topic = new_value

def set_send_topic(new_value):
    global send_topic
    send_topic = new_value

def set_device_port(new_value):
    global device_port
    device_port = new_value

def get_file_name():
    return file_name

def get_file_directory():
    return file_directory

def get_ssid():
    return ssid

def get_password():
    return password

def get_ip_esp32():
    return ip_esp32

def get_mqtt_client_name():
    return mqtt_client_name

def get_mqtt_server():
    return mqtt_server

def get_mqtt_port():
    return mqtt_port

def get_receive_topic():
    return receive_topic

def get_send_topic():
    return send_topic

def get_device_port():
    return device_port