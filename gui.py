from data import set_training_path, set_validation_path
from utils import save_values_page1, save_values_page2, create_numeric_entry, raise_frame, create_sketch_async, get_port_list
from model import train_async
from template import get_arduino_code, set_arduino_code
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
import threading
from tkinter.ttk import *

class GUI(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('TFG José Talavera Pulido')
        root = ctk.CTkFrame(self)  
        root.pack(side="top", fill="both", expand=True)
        ctk.set_appearance_mode("dark") 
        ctk.set_default_color_theme("blue")
        

        # Center a window on the screen
        window_width = 1080
        window_height = 720
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

        # Configuring grid layout for the root window
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
  
        self.frames = {}

        frame = Page1(root, self)
        self.frames[Page1] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        frame = Page3(root, self)
        model_entry = frame.get_model_entry()
        self.frames[Page3] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        frame = Page2(root, self, model_entry)
        self.frames[Page2] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        frame = Page4(root, self)
        self.frames[Page4] = frame
        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Page1)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        self.update_idletasks()  # Forzar la actualización del GUI

        


class Page1(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        # Grid layout configuration for page 1, 7 rows and 6 columns
        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
            
        for i in range(6):  
            self.grid_columnconfigure(i, weight=1)

        # Textbox for entering model architecture
        self.model_entry = ctk.CTkTextbox(master=self, font=("helvetica", 15))
        self.model_entry.grid(row=0, column=0, padx=20, pady=20, rowspan=3, columnspan=6, sticky="nsew")  

        # Labels and entry fields for batch size, epochs, and Adam learning rate
        self.batch_size_label = ctk.CTkLabel(self, text="Batch Size:", font=("helvetica", 13))
        self.batch_size_label.grid(row=3, column=0, padx=20, sticky='e')  

        self.batch_size_entry = create_numeric_entry(self, 'int', data_length=4)  
        self.batch_size_entry.grid(row=3, column=1, padx=20, sticky='w')  

        self.epochs_label = ctk.CTkLabel(self, text="Epochs:", font=("helvetica", 13))
        self.epochs_label.grid(row=3, column=2, padx=20, sticky='e')

        self.epochs_entry = create_numeric_entry(self, 'int', data_length=4)  
        self.epochs_entry.grid(row=3, column=3, padx=20, sticky='w')

        self.adam_learning_rate_label = ctk.CTkLabel(self, text="Adam Learning Rate:", font=("helvetica", 13))
        self.adam_learning_rate_label.grid(row=3, column=4, padx=20, sticky='e')

        self.adam_learning_rate_entry = create_numeric_entry(self, 'float', data_length=6)  
        self.adam_learning_rate_entry.grid(row=3, column=5, padx=20, sticky='w')

        # Button to create model and proceed to next page
        self.create_model_btn = ctk.CTkButton(self, text="Create Model", font=("helvetica", 13), command=lambda: save_values_page1(controller, Page2, self.model_entry, self.batch_size_entry, self.epochs_entry, self.adam_learning_rate_entry), width=50)        
        self.create_model_btn.grid(row=6, column=0, columnspan=6, padx=20, pady=20)  

        
  
class Page2(ctk.CTkFrame):
    def __init__(self, parent, controller, model_entry):
        super().__init__(parent)

        # Grid layout configuration for page 2, 10 rows and 2 columns
        for i in range(11):  
            self.grid_rowconfigure(i, weight=1)

        for i in range(2):  
            self.grid_columnconfigure(i, weight=1)
            
        self.model_entry = model_entry  

        # Entry fields for user input
        self.file_name_label = ctk.CTkLabel(self, text="File name:")
        self.file_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  

        self.file_name_entry = ctk.CTkEntry(self)
        self.file_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w") 

        self.ssid_label = ctk.CTkLabel(self, text="SSID:")
        self.ssid_label.grid(row=1, column=0, padx=10, pady=10, sticky="e") 

        self.ssid_entry = ctk.CTkEntry(self)
        self.ssid_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")  

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")  

        # Entry field for password, showing bullet characters for security
        self.password_entry = ctk.CTkEntry(self, show="•")
        self.password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w") 

        self.ip_esp32_label = ctk.CTkLabel(self, text="ESP32 IP:")
        self.ip_esp32_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")  

        self.ip_esp32_entry = ctk.CTkEntry(self)
        self.ip_esp32_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")  

        self.mqtt_client_name_label = ctk.CTkLabel(self, text="MQTT Client Name:")
        self.mqtt_client_name_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")  

        self.mqtt_client_name_entry = ctk.CTkEntry(self)
        self.mqtt_client_name_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w") 

        self.mqtt_server_label = ctk.CTkLabel(self, text="MQTT Server:")
        self.mqtt_server_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")  

        self.mqtt_server_entry = ctk.CTkEntry(self)
        self.mqtt_server_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w") 

        self.mqtt_port_label = ctk.CTkLabel(self, text="MQTT Port:")
        self.mqtt_port_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")  

        # Entry field for MQTT port, restrict input to integers
        self.mqtt_port_entry = create_numeric_entry(self, 'int', data_length=4)
        self.mqtt_port_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w") 

        self.receive_topic_label = ctk.CTkLabel(self, text="Receive Topic:")
        self.receive_topic_label.grid(row=7, column=0, padx=10, pady=10, sticky="e") 

        self.receive_topic_entry = ctk.CTkEntry(self)
        self.receive_topic_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")  

        self.send_topic_label = ctk.CTkLabel(self, text="Send Topic:")
        self.send_topic_label.grid(row=8, column=0, padx=10, pady=10, sticky="e")  

        self.send_topic_entry = ctk.CTkEntry(self)
        self.send_topic_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")  


        # Dropdown menu for device port selection
        self.dropdown_label = ctk.CTkLabel(self, text="Device Port:")
        self.dropdown_label.grid(row=9, column=0, padx=10, pady=10, sticky="e")  

        # Get the list of available ports and set the default value
        port_list = get_port_list()
        self.port_clicked = ctk.StringVar(value = port_list[0])

        # Dropdown menu to display available ports
        self.dropdown_menu = ctk.CTkOptionMenu(self, variable = self.port_clicked, values = port_list)
        self.dropdown_menu.grid(row=9, column=1, padx=10, pady=10, sticky="w")  

        # MODIFICAR MODEL_ENTRY
        self.model_entry.insert("1.0", "Texto insertado desde Page2")

        # Buttons for navigation and compiling/deploying   
        self.edit_config_btn = ctk.CTkButton(self, text="Edit Configuration", command=lambda: controller.show_frame(Page1))
        self.edit_config_btn.grid(row=10, column=0, padx=50, pady=10, sticky="ew")  

        self.compile_btn = ctk.CTkButton(self, text="Compile and Deploy", command=lambda: save_values_page2(controller, Page3, self.file_name_entry, self.ssid_entry, self.password_entry, self.ip_esp32_entry,
                                                                                                        self.mqtt_client_name_entry, self.mqtt_server_entry, self.mqtt_port_entry,
                                                                                                        self.receive_topic_entry, self.send_topic_entry, self.port_clicked, self.model_entry))
        
        self.compile_btn.grid(row=10, column=1, padx=50, pady=10, sticky="ew")


  
class Page3(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)  # Añadido para asegurar que ambas columnas se expandan uniformemente


        # Model entry
        self.model_entry = ctk.CTkTextbox(self, font=("helvetica",15))
        self.model_entry.grid(row=0, column=0, padx=20, pady=20, columnspan=2, sticky="nsew")  
        
        # Button to navigate back to the previous page
        self.back_button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(Page2))
        self.back_button.grid(row=1, column=0, padx=50, pady=10, sticky="ew")

        # Button to create model and proceed to next page 
        self.create_model_btn = ctk.CTkButton(self, text="Create Model", font=("helvetica",13),  command=lambda: (controller.show_frame(Page4), set_arduino_code(self.model_entry.get("1.0",'end-1c'))))
        self.create_model_btn.grid(row=1, column=1, padx=50, pady=10, sticky="ew")


    def get_model_entry(self):
        return self.model_entry


class Page4(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        for i in range(5): 
            self.grid_rowconfigure(i, weight=1)

        for i in range(3): 
            self.grid_columnconfigure(i, weight=1)

        # Creating console text area
        self.console_text = ScrolledText(self, bg="black", fg="white")
        self.console_text.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")  

        # Label to display selected training data file
        self.train_file_label = ctk.CTkLabel(self, text="No file chosen")
        self.train_file_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # Button to open CSV file for training data
        self.open_train_dataset_btn = ctk.CTkButton(self, text="Open Training Data File", command=lambda: set_training_path(self.train_file_label, self.train_model_button))
        self.open_train_dataset_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Label to display selected validation data file
        self.validation_file_label = ctk.CTkLabel(self, text="No file chosen")
        self.validation_file_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # Button to open CSV file for validation data
        self.open_val_dataset_btn = ctk.CTkButton(self, text="Open Validation Data File", command=lambda: set_validation_path(self.validation_file_label, self.train_model_button))
        self.open_val_dataset_btn.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Button to open CSV file for validation data
        self.progress_bar  = Progressbar(self)
        #self.progress_bar.grid(row=4, column=1, padx=10, pady=10, sticky="ew")
        self.progress_bar_label = ctk.CTkLabel(self, text="Training model...")
        #self.progress_bar_label.grid(row=4, column=2, padx=10, pady=10, sticky="e")  
        


        # Button to navigate back to the previous page
        self.back_button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(Page3))
        self.back_button.grid(row=4, column=0, padx=30, pady=5, sticky="ew")  

        # Button to train the model
        self.train_model_button = ctk.CTkButton(self, text="Train model", command=lambda: train_async(self.console_text, self.upload_sketch_button, self.progress_bar, self.progress_bar_label))
        self.train_model_button.grid(row=4, column=1, padx=30, pady=5, sticky="ew")

        # Button to upload the sketch
        self.upload_sketch_button = ctk.CTkButton(self, text="Compile & Upload Sketch", command=lambda: create_sketch_async(self.console_text))
        self.upload_sketch_button.grid(row=4, column=2, padx=30, pady=5, sticky="ew")  

        # Disable train model button until model is trained
        self.train_model_button.configure(state='disabled')

        # Disable upload sketch button until model is trained
        self.upload_sketch_button.configure(state='disabled')

