from model import set_model, set_batch_size, set_epochs, set_adam_learning_rate, get_cpp_code
import subprocess
from user_input import set_file_name,set_file_directory,set_ssid,set_password,set_ip_esp32,set_mqtt_client_name,set_mqtt_server,set_mqtt_port,set_receive_topic,set_send_topic, set_device_port
from user_input import get_file_name,get_file_directory,get_password,get_ip_esp32, get_device_port
from template import set_arduino_code_template, get_arduino_code
from config import MODELS_DIRECTORY, FQBN_ESP32
import re
import threading
import customtkinter as ctk
from tkinter import messagebox
import ipaddress


def validate_input(new_value, data_type, data_length=None):
    if new_value == "":
        return True
    try:
        if data_length is not None and len(new_value) > data_length:
            return False  
        if data_type == 'int':
            int(new_value)
        elif data_type == 'float':
            float(new_value)
        return True
    except ValueError:
        return False

def create_numeric_entry(parent, data_type, data_length=None):
    vcmd = parent.register(lambda new_value: validate_input(new_value, data_type, data_length))
    entry = ctk.CTkEntry(parent, validate="key", validatecommand=(vcmd, '%P'))
    return entry

def update_progress(progress_bar, progress_label, value, message):
    progress_bar['value'] = value  # Ajusta el valor de la barra de progreso
    progress_label.configure(text=message)  # Cambia el texto del label
    progress_bar.update_idletasks()  # Actualiza la barra de progreso en la GUI

def get_port_list():
    result = subprocess.run('arduino-cli board list', capture_output=True, text=True, shell=True)

    if result.returncode == 0:
        output = result.stdout
        print(output)

        lines = output.strip().split('\n')
        
        # Create a list with the desired format: COMx-Protocol
        port_list = [line.split()[0] + '-' + line.split()[1] for line in lines[1:]]
        
        print("port_list: ", port_list)
    else:
        print("Error executing the command.")

    return port_list


def raise_frame(frame_list, target_frame):
    for frame in frame_list:
        frame.grid_remove()

    target_frame.grid()



def create_sketch_async(console_text,progress_bar, progress_bar_label):    
    # Create a thread to execute create_sketch()
    train_thread = threading.Thread(target=create_sketch, args=(console_text,progress_bar, progress_bar_label))
    train_thread.start()
    

def upload_sketch_async(command, cwd, console_text, progress_bar, progress_bar_label):
    def run_command():
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd, universal_newlines=True, bufsize=1)

        # Read command output line by line
        with process.stdout:
            for line in iter(process.stdout.readline, ''):
                console_text.insert('end', line)
                console_text.see('end')  # Automatically move the scrollbar to the end
                if "Done" in line:
                    update_progress(progress_bar, progress_bar_label, 100, "Upload completed")

        # Ensure the process is closed properly
        process.stdout.close()
        process.wait()
    
    # Start the thread to handle real-time output
    thread = threading.Thread(target=run_command)
    thread.start()






def create_sketch(console_text, progress_bar, progress_bar_label):    
    console_text.delete("1.0", 'end-1c')
    progress_bar['value'] = 0

    # Inicializa la barra de progreso
    update_progress(progress_bar, progress_bar_label, 0, "Creating sketch...")

    # Create Sketch
    file_name = get_file_name()
    create_sketch_command = f"arduino-cli sketch new {file_name}"
    try:
        process = subprocess.Popen(create_sketch_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=MODELS_DIRECTORY)
        stdout, stderr = process.communicate()
        update_progress(progress_bar, progress_bar_label, 20, "Creating .ino file...")
    except Exception as e:
        console_text.insert('end', str(e) + "\n")

    # Create .ino file
    arduino_code = get_arduino_code()
    try:
        with open(MODELS_DIRECTORY + f"\\{file_name}\\{file_name}.ino", "w") as archivo:
            archivo.write(arduino_code)
        update_progress(progress_bar, progress_bar_label, 40, "Creating header file...")
    except Exception as e:
        console_text.insert('end', str(e) + "\n")

    # Create model.h file
    cpp_code = get_cpp_code()
    try:
        with open(MODELS_DIRECTORY + f"\\{file_name}\\model.h", "w") as archivo:
            archivo.write(cpp_code)
        update_progress(progress_bar, progress_bar_label, 60, "Compiling sketch")
    except Exception as e:
        console_text.insert('end', str(e) + "\n")

    # Compile Sketch
    console_text.insert('end', "REMEMBER: HOLD DOWN BOOT MODE BUTTON IN DEVICE WHEN UPLOADING\n")
    file_directory = get_file_directory()
    compile_command = f"arduino-cli compile --fqbn {FQBN_ESP32} {file_name}.ino"
    try:
        process = subprocess.Popen(compile_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=file_directory)
        stdout, stderr = process.communicate()
        output = stdout.decode("utf-8") + stderr.decode("utf-8")
        console_text.insert('end', output)
        update_progress(progress_bar, progress_bar_label, 80, "Uploading sketch...")
    except Exception as e:
        console_text.insert('end', str(e) + "\n")

    # Upload Sketch
    device_port = get_device_port()
    port, protocol = device_port.split("-")
    password = get_password()

    if "NETWORK" in protocol.upper():
        ip_esp32 = get_ip_esp32()
        upload_command = f"arduino-cli upload -p {ip_esp32} --fqbn {FQBN_ESP32} --upload-field password={password} {file_name}.ino"
    elif "SERIAL" in protocol.upper():
        upload_command = f"arduino-cli upload -p {port} --fqbn {FQBN_ESP32} {file_name}.ino"

    upload_sketch_async(upload_command, file_directory, console_text, progress_bar, progress_bar_label)






def setters_values_page1(model_str,batch_size,epochs,adam_learning_rate):
    set_model(model_str)
    set_batch_size(batch_size)
    set_epochs(epochs)
    set_adam_learning_rate(adam_learning_rate)

    print("model_str: ", model_str)
    print("Batch size:", batch_size)
    print("Epochs:", epochs)
    print("Adam learning rate:", adam_learning_rate)


def save_values_page1(controller, Page2, model_entry, batch_size_entry, epochs_entry, adam_learning_rate_entry):
    
    model_str = model_entry.get(1.0, 'end').strip()
    batch_size = batch_size_entry.get()
    epochs = epochs_entry.get()
    adam_learning_rate = adam_learning_rate_entry.get()

    # Regular expression to verify the format of the model text
    model_pattern = r"model\s*=\s*tf\.keras\.Sequential\(\[\s*(?:.*,\s*)*.*\s*\]\s*\)"

    # Check if the model field is empty
    if not model_str or not all([batch_size, epochs, adam_learning_rate]):
        messagebox.showerror("Error", "Please fill in all fields")
        return

    # Check if the model text matches the pattern
    elif not re.match(model_pattern, model_str):
        messagebox.showerror("Error", "The model does not have the expected structure.")
        return
    else:

        # Check that the values of batch size, epochs, and Adam learning rate are numeric and within the allowed range
        try:
            batch_size = int(batch_size)

            if not (1 <= batch_size <= 4096):
                raise ValueError("Batch size must be between 1 and 4096.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            epochs = int(epochs)

            if not (1 <= epochs <= 1000):
                raise ValueError("Epochs must be between 1 and 1000.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        try:
            adam_learning_rate = float(adam_learning_rate)

            if not (0.0001 <= adam_learning_rate <= 0.1):
                raise ValueError("Adam learning rate must be between 0.1 and 0.0001.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return


        threading.Thread(target=lambda:setters_values_page1(model_str,batch_size,epochs,adam_learning_rate)).start()
        controller.show_frame(Page2)

        


def set_model_entry_page3(model_entry):
    arduino_code = get_arduino_code()
    
    # Configure format for predefined text
    model_entry.tag_config('predefined', foreground='#7BC9FF')

    # Insert predefined text
    model_entry.delete("1.0", 'end')
    model_entry.insert("1.0", arduino_code, 'predefined')

    # Function to apply format to user-entered text
    def apply_format(event):
        # If keyboard event is not from predefined text
        if model_entry.index("insert") != "1.0":
            # Remove any previous formatting and set color directly to white
            model_entry.tag_remove('predefined', "insert linestart", "insert lineend")
            model_entry.tag_config('insert', foreground='white')  # White color for user text

    # Capture keyboard event
    model_entry.bind("<Key>", apply_format)
    


def save_values_page2(controller, Page3, file_name_entry, ssid_entry, password_entry, ip_esp32_entry,
                mqtt_client_name_entry, mqtt_server_entry, mqtt_port_entry,
                receive_topic_entry, send_topic_entry, port_clicked_entry, model_entry):
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

    # Check if ip_esp32 is a valid IPv4
    try:
        ipaddress.ip_address(ip_esp32)
    except ValueError as e:
        messagebox.showerror("Error", str(e))
        return

    # Check if any field is empty or if mqtt_port is not valid
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
        set_arduino_code_template(ssid, password, mqtt_client_name, mqtt_server, mqtt_port, receive_topic, send_topic)
        
        
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

        set_model_entry_page3(model_entry) 

        controller.show_frame(Page3)
