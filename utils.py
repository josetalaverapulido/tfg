from model import set_model, set_batch_size, set_epochs, set_adam_learning_rate, cpp_code
import tkinter as tk
from tkinter import Entry, messagebox
import subprocess

from user_input import set_file_name,set_file_directory,set_ssid,set_password,set_ip_esp32,set_mqtt_client_name,set_mqtt_server,set_mqtt_port,set_receive_topic,set_send_topic, set_device_port
from user_input import get_file_name,get_file_directory,get_ssid,get_password,get_ip_esp32,get_mqtt_client_name,get_mqtt_server,get_mqtt_port,get_receive_topic,get_send_topic, get_device_port
from template import prueba
from config import MODELS_DIRECTORY, FQBN_ESP32
import re


def validate_input(new_value, data_type, data_length=None):
    if new_value == "":
        return True
    try:
        if data_length is not None and len(new_value) > data_length:
            return False  # Si el valor es más largo que la longitud máxima, retorna False
        if data_type == 'int':
            int(new_value)
        elif data_type == 'float':
            float(new_value)
        return True
    except ValueError:
        return False


def create_numeric_entry(parent, data_type, data_length=None):
    vcmd = parent.register(lambda new_value: validate_input(new_value, data_type, data_length))
    entry = Entry(parent, validate="key", validatecommand=(vcmd, '%P'))
    return entry


def get_port_list():
    # Run the command in the cmd
    result = subprocess.run('arduino-cli board list', capture_output=True, text=True, shell=True)

    # Check if the execution was successful
    if result.returncode == 0:
        # Get the output of the command
        output = result.stdout
        
        # Print the output to verify
        print(output)
        
        # Separate the output lines
        lines = output.strip().split('\n')
        
        # Create a list with the desired format: COMx-Protocol
        port_list = [line.split()[0] + '-' + line.split()[1] for line in lines[1:]]
        
        # Print the port list
        print("port_list: ", port_list)
    else:
        print("Error executing the command.")

    return port_list

# raise_frame([frame1, frame3], frame2))

def raise_frame(frame_list, target_frame):
    for frame in frame_list:
        frame.grid_remove()

    target_frame.grid()



def create_sketch_async(console_text):    
    # Crear un hilo para ejecutar create_sketch()
    train_thread = threading.Thread(target=create_sketch, args=(console_text))
    train_thread.start()



def create_sketch(console_text):    

    #----------------- Crear Sketch --------------
    file_name = get_file_name()
    
    create_sketch_command = f"arduino-cli sketch new {file_name}"
    try:
        process = subprocess.Popen(create_sketch_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=MODELS_DIRECTORY)
        console_text.insert('end', "\nSketch created succesfully\n")
    except Exception as e:
        console_text.insert('end', str(e) + "\n")

    #----------------- Crear .ino --------------
    ssid = get_ssid()
    password = get_password()
    mqtt_client_name = get_mqtt_client_name()
    mqtt_server = get_mqtt_server()
    mqtt_port = get_mqtt_port()
    receive_topic = get_receive_topic()
    send_topic = get_send_topic()

    codigo_arduino = prueba(ssid, password, mqtt_client_name, mqtt_server, mqtt_port, receive_topic, send_topic)
    with open(MODELS_DIRECTORY + f"\{file_name}\{file_name}.ino", "w") as archivo:
        archivo.write(codigo_arduino)
    print("archivo .ino creado correctamente \n")


    #----------------- Crear modelo.h --------------
    with open(MODELS_DIRECTORY + f"\{file_name}\model.h", "w") as archivo:
        archivo.write(cpp_code)
    print("archivo .h creado correctamente\n")

 
    #----------------- Compila Sketch --------------
    file_directory = get_file_directory()
    compile_command = f"arduino-cli compile --fqbn {FQBN_ESP32} {file_name}.ino"

    try:
        process = subprocess.Popen(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=file_directory)
        stdout, stderr = process.communicate()
        output = stdout.decode("latin1") + stderr.decode("latin1")
        console_text.insert('end', output)
    except Exception as e:
        console_text.insert('end', str(e) + "\n")


    #----------------- Carga Sketch --------------
    device_port = get_device_port()
    port, protocol = device_port.split("-")

    if "NETWORK" in protocol.upper():
        ip_esp32 = get_ip_esp32()
        upload_command = f"arduino-cli upload -p {ip_esp32} --fqbn {FQBN_ESP32} --upload-field password={password} {file_name}.ino"

    elif "SERIAL"in protocol.upper():
        upload_command = f"arduino-cli upload -p {port} --fqbn {FQBN_ESP32} {file_name}.ino"
    
    try:
        process = subprocess.Popen(upload_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=file_directory)
        stdout, stderr = process.communicate()
        output = stdout.decode("latin1") + stderr.decode("latin1")
        console_text.delete('end-2l', 'end')  # Elimina la última línea antes de agregar el nuevo texto
        console_text.insert('end',"\n\n" + output)
    except Exception as e:
        console_text.insert('end', str(e) + "\n")






def save_values_page1(frame_list, target_frame, model_entry):
    # Obtener el texto del widget Text
    model_str = model_entry.get(1.0, 'end').strip()

    # Expresión regular para verificar el formato del texto del modelo
    model_pattern = r"model\s*=\s*tf\.keras\.Sequential\(\[\s*(?:.*,\s*)*.*\s*\]\s*\)"

    # Verificar si el campo del modelo está vacío
    if not model_str:
        messagebox.showerror("Error", "Please fill the field")
        return
    

    # Verificar si el texto del modelo coincide con el patrón
    if not re.match(model_pattern, model_str):
        messagebox.showerror("Error", "The model does not have the expected structure.")
        return


    set_model(model_str)
    print("model_str: ", model_str)
    # Llamar a la función para cambiar al frame 2
    raise_frame(frame_list, target_frame)



def save_values_page2(frame_list, target_frame, batch_size_entry, epochs_entry, adam_learning_rate_entry):
    batch_size = batch_size_entry.get()
    epochs = epochs_entry.get()
    adam_learning_rate = adam_learning_rate_entry.get()


    # Verificar si hay campos vacíos
    if not all([batch_size, epochs, adam_learning_rate]):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    else:
        set_batch_size(batch_size)
        set_epochs(epochs)
        set_adam_learning_rate(adam_learning_rate)

        print("Batch size:", batch_size)
        print("Epochs:", epochs)
        print("Adam learning rate:", adam_learning_rate)

        # Llamar a la función para cambiar al frame 3
        raise_frame(frame_list, target_frame)



def save_values_page3(frame_list,target_frame,file_name_entry, ssid_entry, password_entry, ip_esp32_entry,
                mqtt_client_name_entry, mqtt_server_entry, mqtt_port_entry,
                receive_topic_entry, send_topic_entry, port_clicked_entry):
    file_name = file_name_entry.get()
    ssid = ssid_entry.get()
    password = password_entry.get()
    ip_esp32 = ip_esp32_entry.get()
    mqtt_client_name = mqtt_client_name_entry.get()
    mqtt_server = mqtt_server_entry.get()
    mqtt_port = mqtt_port_entry.get()
    receive_topic = receive_topic_entry.get()
    send_topic = send_topic_entry.get()
    device_port = port_clicked_entry.get()


    # Verificar si algún campo está vacío o si mqtt_port no es válido
    if '' in [file_name, ssid, password, ip_esp32, mqtt_client_name, mqtt_server, mqtt_port, receive_topic, send_topic] \
            or not validate_input(mqtt_port, 'int', data_length=4):
        messagebox.showerror("Error", "Please fill in all fields")

        return
    else:
        set_file_name(file_name)
        set_file_directory(file_name)
        set_ssid(ssid)
        set_password(password)
        set_ip_esp32(ip_esp32)
        set_mqtt_client_name(mqtt_client_name)
        set_mqtt_server(mqtt_server)
        set_mqtt_port(mqtt_port)
        set_receive_topic(receive_topic)
        set_send_topic(send_topic)
        set_device_port(device_port)


        print("File Name:", file_name)
        print("SSID:", ssid)
        print("Password:", password)
        print("IP ESP32:", ip_esp32)
        print("MQTT Client Name:", mqtt_client_name)
        print("MQTT Server:", mqtt_server)
        print("MQTT Port:", mqtt_port)
        print("Receive Topic:", receive_topic)
        print("Send Topic:", send_topic)
        print("Device Port:", device_port)


        raise_frame(frame_list, target_frame)
