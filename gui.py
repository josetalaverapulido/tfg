from data import set_training_path, set_validation_path
import os
from config import *
from user_input import *
from utils import save_values_page1,save_values_page2, save_values_page3, create_numeric_entry, raise_frame, create_sketch, get_port_list
from model import train_async
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText


ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")


# Initializing the Tkinter root window
root = ctk.CTk()
root.title('TFG José Talavera Pulido')  # Setting title
#root.resizable(False,False) # Disabling window resizing


# Center a window on the screen
window_width = 1080
window_height = 720
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_cordinate = int((screen_width/2) - (window_width/2))
y_cordinate = int((screen_height/2) - (window_height/2))
root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))


# Configuring grid layout for the root window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)


# Creating frames for different pages
page1 = ctk.CTkFrame(root)
page2 = ctk.CTkFrame(root)
page3 = ctk.CTkFrame(root)
page4 = ctk.CTkFrame(root)


# Grid layout configuration for the frames
page1.grid(row=0, column=0, sticky="nsew")
page2.grid(row=0, column=0, sticky="nsew")
page3.grid(row=0, column=0, sticky="nsew")
page4.grid(row=0, column=0, sticky="nsew")




# Function to create Page 1 elements
def create_page1():
    # Grid layout configuration for page 1, 7 rows and 6 columns
    for i in range(7):
        page1.grid_rowconfigure(i, weight=1)

    for i in range(6):  
        page1.grid_columnconfigure(i, weight=1)

    model_entry = ctk.CTkTextbox(master = page1, font=("helvetica",15))
    model_entry.grid(row=0, column=0, padx=20, pady=20, rowspan=3, columnspan=6, sticky="nsew")  # Ajusta la ubicación del campo de entrada

    batch_size_label = ctk.CTkLabel(page1, text="Batch Size:", font=("helvetica",13))
    batch_size_label.grid(row=3, column=0, padx=20, sticky='e')  # sticky='e' para alinear el texto a la derecha

    batch_size_entry = create_numeric_entry(page1, 'int', data_length=3)
    batch_size_entry.grid(row=3, column=1,padx=20,  sticky='w')  # sticky='w' para alinear el widget a la izquierda

    epochs_label = ctk.CTkLabel(page1, text="Epochs:", font=("helvetica",13))
    epochs_label.grid(row=3, column=2, padx=20, sticky='e')

    epochs_entry = create_numeric_entry(page1, 'int', data_length=4)
    epochs_entry.grid(row=3, column=3, padx=20, sticky='w')

    adam_learning_rate_label = ctk.CTkLabel(page1, text="Adam Learning Rate:", font=("helvetica",13))
    adam_learning_rate_label.grid(row=3, column=4, padx=20, sticky='e')

    adam_learning_rate_entry = create_numeric_entry(page1, 'float', data_length=6)
    adam_learning_rate_entry.grid(row=3, column=5, padx=20, sticky='w')

    create_model_btn = ctk.CTkButton(page1, text="Create Model", font=("helvetica",13), command=lambda: [save_values_page1([page1, page2, page3, page4], page2, model_entry, batch_size_entry, epochs_entry, adam_learning_rate_entry)], width=50)
    create_model_btn.grid(row=6, column=0, columnspan=6, padx=20, pady=20)  # Ajusta la ubicación del botón




# Function to create Page 2 elements
def create_page2():

    # Grid layout configuration for page 2, 7 rows and 2 columns
    for i in range(7):
        page2.grid_rowconfigure(i, weight=1)

    for i in range(2):  
        page2.grid_columnconfigure(i, weight=1)


    # Creating labels and entry widgets for configuration options
    batch_size_label = ctk.CTkLabel(page2, text="Batch Size:")
    batch_size_label.grid(row=1, column=0, padx=10, pady=10, sticky="e") 

    batch_size_entry = create_numeric_entry(page2, 'int', data_length=3)
    batch_size_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")  

    epochs_label = ctk.CTkLabel(page2, text="Epochs:")
    epochs_label.grid(row=2, column=0, padx=10, pady=10, sticky="e") 

    epochs_entry = create_numeric_entry(page2, 'int', data_length=4)
    epochs_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")  

    adam_learning_rate_label = ctk.CTkLabel(page2, text="Adam Learning Rate:")
    adam_learning_rate_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")  

    adam_learning_rate_entry = create_numeric_entry(page2, 'float', data_length=6)
    adam_learning_rate_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")  



    # Creating page 2 buttons    
    modify_model_btn = ctk.CTkButton(page2, text="Modify Model", command=lambda: raise_frame([page1,page2,page3,page4],page1))
    modify_model_btn.grid(row=7, column=0, padx=50, pady=20, sticky="ew")

    submit_config_btn = ctk.CTkButton(page2, text="Submit Configuration", command=lambda: save_values_page2([page1,page2,page3,page4],page3,batch_size_entry, epochs_entry, adam_learning_rate_entry))
    submit_config_btn.grid(row=7, column=1, padx=50, pady=20, sticky="ew")




# Function to create Page 3 elements
def create_page3():
    
    # Grid layout configuration for page 2, 10 rows and 2 columns
    for i in range(11):  
        page3.grid_rowconfigure(i, weight=1)

    for i in range(2):  
        page3.grid_columnconfigure(i, weight=1)


    file_name_label = ctk.CTkLabel(page3, text="File name:")
    file_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  

    file_name_entry = ctk.CTkEntry(page3)
    file_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w") 

    ssid_label = ctk.CTkLabel(page3, text="SSID:")
    ssid_label.grid(row=1, column=0, padx=10, pady=10, sticky="e") 

    ssid_entry = ctk.CTkEntry(page3)
    ssid_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")  

    password_label = ctk.CTkLabel(page3, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")  

    password_entry = ctk.CTkEntry(page3, show="•")
    password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w") 

    ip_esp32_label = ctk.CTkLabel(page3, text="ESP32 IP:")
    ip_esp32_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")  

    ip_esp32_entry = ctk.CTkEntry(page3)
    ip_esp32_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")  

    mqtt_client_name_label = ctk.CTkLabel(page3, text="MQTT Client Name:")
    mqtt_client_name_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")  

    mqtt_client_name_entry = ctk.CTkEntry(page3)
    mqtt_client_name_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w") 

    mqtt_server_label = ctk.CTkLabel(page3, text="MQTT Server:")
    mqtt_server_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")  

    mqtt_server_entry = ctk.CTkEntry(page3)
    mqtt_server_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w") 

    mqtt_port_label = ctk.CTkLabel(page3, text="MQTT Port:")
    mqtt_port_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")  

    mqtt_port_entry = create_numeric_entry(page3, 'int', data_length=4)
    mqtt_port_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w") 

    receive_topic_label = ctk.CTkLabel(page3, text="Receive Topic:")
    receive_topic_label.grid(row=7, column=0, padx=10, pady=10, sticky="e") 

    receive_topic_entry = ctk.CTkEntry(page3)
    receive_topic_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")  

    send_topic_label = ctk.CTkLabel(page3, text="Send Topic:")
    send_topic_label.grid(row=8, column=0, padx=10, pady=10, sticky="e")  

    send_topic_entry = ctk.CTkEntry(page3)
    send_topic_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")  


    # Dropdown menu
    dropdown_label = ctk.CTkLabel(page3, text="Device Port:")
    dropdown_label.grid(row=9, column=0, padx=10, pady=10, sticky="e")  

    
    port_list = get_port_list()
    port_clicked = ctk.StringVar(value = port_list[0])

    dropdown_menu = ctk.CTkOptionMenu(page3, variable = port_clicked, values = port_list)
    dropdown_menu.grid(row=9, column=1, padx=10, pady=10, sticky="w")  

    # Creating page 3 buttons    
    edit_config_btn = ctk.CTkButton(page3, text="Edit Configuration", command=lambda: raise_frame([page1,page2,page3,page4],page2))
    edit_config_btn.grid(row=10, column=0, padx=50, pady=10, sticky="ew")  

    compile_btn = ctk.CTkButton(page3, text="Compile and Deploy", command=lambda: save_values_page3([page1,page2,page3,page4], page4,file_name_entry, ssid_entry, password_entry,
                                                                    ip_esp32_entry, mqtt_client_name_entry, mqtt_server_entry, mqtt_port_entry,
                                                                    receive_topic_entry, send_topic_entry, port_clicked))

    compile_btn.grid(row=10, column=1, padx=50, pady=10, sticky="ew")  




# Function to create Page 4 elements
def create_page4():
    for i in range(4): 
        page4.grid_rowconfigure(i, weight=1)

    for i in range(3): 
        page4.grid_columnconfigure(i, weight=1)

    # Creating console text area and buttons for actions
    
    console_text = ScrolledText(page4, bg="black", fg="white")
    console_text.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")  

    # Crear un recuadro de texto para mostrar la información del archivo seleccionado
    train_file_label = ctk.CTkLabel(page4, text="No file chosen")
    train_file_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

    # Button to open CSV file
    open_train_dataset_btn = ctk.CTkButton(page4, text="Open Training Data File", command=lambda: set_training_path(train_file_label, train_model_button))
    open_train_dataset_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

    # Crear un recuadro de texto para mostrar la información del archivo seleccionado
    validation_file_label = ctk.CTkLabel(page4, text="No file chosen")
    validation_file_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

    # Button to open CSV file
    open_val_dataset_btn = ctk.CTkButton(page4, text="Open Validation Data File", command=lambda: set_validation_path(validation_file_label, train_model_button))
    open_val_dataset_btn.grid(row=2, column=1, padx=10, pady=10, sticky="ew")


    back_button = ctk.CTkButton(page4, text="Back", command=lambda: raise_frame([page1,page2,page3,page4],page3))
    back_button.grid(row=3, column=0, padx=30, pady=5, sticky="ew")  

    train_model_button = ctk.CTkButton(page4, text="Train model", command=lambda: train_async(console_text, upload_sketch_button))
    train_model_button.grid(row=3, column=1, padx=30, pady=5, sticky="ew")  

    upload_sketch_button = ctk.CTkButton(page4, text="Upload Sketch", command=lambda: create_sketch(console_text))
    upload_sketch_button.grid(row=3, column=2, padx=30, pady=5, sticky="ew")  
    

    # Disable button until model is trained
    train_model_button.configure(state='disabled')

    # Disable button until model is trained
    upload_sketch_button.configure(state='disabled')


    


# Function to display the GUI
def show_gui():

    # Creating elements for all pages
    create_page1()
    create_page2()
    create_page3()
    create_page4()


    # Displaying the first page and centering the window
    raise_frame([page1,page2,page3,page4],page1)

    root.mainloop()