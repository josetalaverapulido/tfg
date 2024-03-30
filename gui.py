from tkinter import *
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam
from keras.losses import MeanSquaredError

from time import sleep

from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

import subprocess


#-----main-----
from data import get_data
import os
import sys
from contextlib import redirect_stdout
from io import StringIO
from everywhereml.code_generators.tensorflow import tf_porter
from template import prueba

#-----main-----




from config import *
from user_input import *
from utils import save_values_page1,save_values_page2, save_values_page3, create_numeric_entry, raise_frame, create_sketch
from model import train_async




 

# Initializing the Tkinter root window
root = Tk() 
root.title('TFG José Talavera Pulido')  # Setting title
root.geometry("1280x720")  # Setting initial window size
root.resizable(False,False) # Disabling window resizing

# Configuring grid layout for the root window
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Creating frames for different pages
page1 = Frame(root)
page2 = Frame(root)
page3 = Frame(root)
page4 = Frame(root)


# Grid layout configuration for the frames
page1.grid(row=0, column=0, sticky="nsew")
page2.grid(row=0, column=0, sticky="nsew")
page3.grid(row=0, column=0, sticky="nsew")
page4.grid(row=0, column=0, sticky="nsew")




# Function to center a window on the screen
def center_window(window):
    window.update_idletasks()
    width = window.winfo_reqwidth()
    height = window.winfo_reqheight()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))




# Function to create Page 1 elements
def create_page1():
    model_entry = Text(page1, width=100, height=30, font=("Helvetica", 12))
    model_entry.pack(pady=20, padx=20)


    create_model_btn = Button(page1, text="Create Model", command=lambda: [save_values_page1([page1,page2,page3,page4],page2, model_entry)], width=50)
    create_model_btn.pack(pady=20)


# Function to create Page 2 elements
def create_page2():

    # Grid layout configuration for page 2, 7 rows and 2 columns
    for i in range(7):
        page2.grid_rowconfigure(i, weight=1)

    for i in range(2):  
        page2.grid_columnconfigure(i, weight=1)


    # Creating labels and entry widgets for configuration options
    batch_size_label = Label(page2, text="Batch Size:")
    batch_size_label.grid(row=1, column=0, padx=10, pady=10, sticky="e") 

    batch_size_entry = create_numeric_entry(page2, 'int', data_length=3)
    batch_size_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")  

    epochs_label = Label(page2, text="Epochs:")
    epochs_label.grid(row=2, column=0, padx=10, pady=10, sticky="e") 

    epochs_entry = create_numeric_entry(page2, 'int', data_length=4)
    epochs_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")  

    adam_learning_rate_label = Label(page2, text="Adam Learning Rate:")
    adam_learning_rate_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")  

    adam_learning_rate_entry = create_numeric_entry(page2, 'float', data_length=6)
    adam_learning_rate_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")  



    # Creating page 2 buttons    
    modify_model_btn = Button(page2, text="Modify Model", command=lambda: raise_frame([page1,page2,page3,page4],page1))
    modify_model_btn.grid(row=7, column=0, padx=50, pady=20, sticky="ew")

    submit_config_btn = Button(page2, text="Submit Configuration", command=lambda: save_values_page2([page1,page2,page3,page4],page3,batch_size_entry, epochs_entry, adam_learning_rate_entry))
    submit_config_btn.grid(row=7, column=1, padx=50, pady=20, sticky="ew")


# Function to create Page 3 elements
def create_page3():

    # Grid layout configuration for page 2, 10 rows and 2 columns
    for i in range(10):  
        page3.grid_rowconfigure(i, weight=1)

    for i in range(2):  
        page3.grid_columnconfigure(i, weight=1)


    file_name_label = Label(page3, text="File name:")
    file_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  

    file_name_entry = Entry(page3, width=30)
    file_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w") 

    ssid_label = Label(page3, text="SSID:")
    ssid_label.grid(row=1, column=0, padx=10, pady=10, sticky="e") 

    ssid_entry = Entry(page3, width=30)
    ssid_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")  

    password_label = Label(page3, text="Password:")
    password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")  

    password_entry = Entry(page3, width=30)
    password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w") 

    ip_esp32_label = Label(page3, text="ESP32 IP:")
    ip_esp32_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")  

    ip_esp32_entry = Entry(page3, width=30)
    ip_esp32_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")  

    mqtt_client_name_label = Label(page3, text="MQTT Client Name:")
    mqtt_client_name_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")  

    mqtt_client_name_entry = Entry(page3, width=30)
    mqtt_client_name_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w") 
    mqtt_server_label = Label(page3, text="MQTT Server:")
    mqtt_server_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")  

    mqtt_server_entry = Entry(page3, width=30)
    mqtt_server_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w") 

    mqtt_port_label = Label(page3, text="MQTT Port:")
    mqtt_port_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")  

    mqtt_port_entry = create_numeric_entry(page3, 'int', data_length=4)
    mqtt_port_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w") 

    receive_topic_label = Label(page3, text="Receive Topic:")
    receive_topic_label.grid(row=7, column=0, padx=10, pady=10, sticky="e") 

    receive_topic_entry = Entry(page3, width=30)
    receive_topic_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")  

    send_topic_label = Label(page3, text="Send Topic:")
    send_topic_label.grid(row=8, column=0, padx=10, pady=10, sticky="e")  

    send_topic_entry = Entry(page3, width=30)
    send_topic_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")  



    # Creating page 3 buttons    
    edit_config_btn = Button(page3, text="Edit Configuration", command=lambda: raise_frame([page1,page2,page3,page4],page2))
    edit_config_btn.grid(row=9, column=0, padx=50, pady=10, sticky="ew")  

    compile_btn = Button(page3, text="Compile and Deploy", command=lambda: save_values_page3([page1,page2,page3,page4], page4,file_name_entry, ssid_entry, password_entry,
                                                                    ip_esp32_entry, mqtt_client_name_entry, mqtt_server_entry, mqtt_port_entry,
                                                                    receive_topic_entry, send_topic_entry))

    compile_btn.grid(row=9, column=1, padx=50, pady=10, sticky="ew")  




# Function to create Page 4 elements
def create_page4():
    for i in range(3): 
        page4.grid_rowconfigure(i, weight=1)

    for i in range(3): 
        page4.grid_columnconfigure(i, weight=1)

    # Creating console text area and buttons for actions
    console_text = ScrolledText(page4, bg="black", fg="white", width=110)
    console_text.grid(row=0, column=0, columnspan=3, padx=30, pady=10)  

    back_button = Button(page4, text="Back", command=lambda: raise_frame([page1,page2,page3,page4],page3))
    back_button.grid(row=2, column=0, padx=30, pady=5, sticky="ew")  

    train_model_button = Button(page4, text="Train model", command=lambda: train_async(console_text, upload_sketch_button))
    train_model_button.grid(row=2, column=1, padx=30, pady=5, sticky="ew")  

    upload_sketch_button = Button(page4, text="Upload Sketch", command=lambda: create_sketch(console_text))
    upload_sketch_button.grid(row=2, column=2, padx=30, pady=5, sticky="ew")  
    

    # Disable button until model is trained
    upload_sketch_button.config(state='disabled')





# Function to display the GUI
def show_gui():

    # Creating elements for all pages
    create_page1()
    create_page2()
    create_page3()
    create_page4()


    # Displaying the first page and centering the window
    raise_frame([page1,page2,page3,page4],page1)
    center_window(root)

    root.mainloop()