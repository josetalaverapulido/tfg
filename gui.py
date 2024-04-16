from data import set_training_path, set_validation_path
from utils import save_values_page1, save_values_page2, create_numeric_entry, raise_frame, create_sketch, get_port_list
from model import train_async
from template import get_arduino_code, set_arduino_code
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText
import threading


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
        model_entry = ctk.CTkTextbox(master = self, font=("helvetica",15))
        model_entry.grid(row=0, column=0, padx=20, pady=20, rowspan=3, columnspan=6, sticky="nsew")  

        # Labels and entry fields for batch size, epochs, and Adam learning rate
        batch_size_label = ctk.CTkLabel(self, text="Batch Size:", font=("helvetica",13))
        batch_size_label.grid(row=3, column=0, padx=20, sticky='e')  

        batch_size_entry = create_numeric_entry(self, 'int', data_length=3)
        batch_size_entry.grid(row=3, column=1,padx=20,  sticky='w')  

        epochs_label = ctk.CTkLabel(self, text="Epochs:", font=("helvetica",13))
        epochs_label.grid(row=3, column=2, padx=20, sticky='e')

        epochs_entry = create_numeric_entry(self, 'int', data_length=4)
        epochs_entry.grid(row=3, column=3, padx=20, sticky='w')

        adam_learning_rate_label = ctk.CTkLabel(self, text="Adam Learning Rate:", font=("helvetica",13))
        adam_learning_rate_label.grid(row=3, column=4, padx=20, sticky='e')

        adam_learning_rate_entry = create_numeric_entry(self, 'float', data_length=6)
        adam_learning_rate_entry.grid(row=3, column=5, padx=20, sticky='w')

        # Button to create model and proceed to next page
        create_model_btn = ctk.CTkButton(self, text="Create Model", font=("helvetica",13), command=lambda:save_values_page1(controller, Page2, model_entry, batch_size_entry, epochs_entry, adam_learning_rate_entry),  width=50)        
        create_model_btn.grid(row=6, column=0, columnspan=6, padx=20, pady=20)  
        #command=lambda: threading.Thread(target=save_values_page1(controller, Page2, model_entry, batch_size_entry, epochs_entry, adam_learning_rate_entry)).start()

        
  
class Page2(ctk.CTkFrame):
    def __init__(self, parent, controller, model_entry):
        super().__init__(parent)

        # Grid layout configuration for page 2, 10 rows and 2 columns
        for i in range(11):  
            self.grid_rowconfigure(i, weight=1)

        for i in range(2):  
            self.grid_columnconfigure(i, weight=1)
            
        self.model_entry = model_entry  # Guardar model_entry como un atributo de la instancia de Page2

        # Entry fields for user input
        file_name_label = ctk.CTkLabel(self, text="File name:")
        file_name_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")  

        file_name_entry = ctk.CTkEntry(self)
        file_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w") 

        ssid_label = ctk.CTkLabel(self, text="SSID:")
        ssid_label.grid(row=1, column=0, padx=10, pady=10, sticky="e") 

        ssid_entry = ctk.CTkEntry(self)
        ssid_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")  

        password_label = ctk.CTkLabel(self, text="Password:")
        password_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")  

        # Entry field for password, showing bullet characters for security
        password_entry = ctk.CTkEntry(self, show="•")
        password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w") 

        ip_esp32_label = ctk.CTkLabel(self, text="ESP32 IP:")
        ip_esp32_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")  

        ip_esp32_entry = ctk.CTkEntry(self)
        ip_esp32_entry.grid(row=3, column=1, padx=10, pady=10, sticky="w")  

        mqtt_client_name_label = ctk.CTkLabel(self, text="MQTT Client Name:")
        mqtt_client_name_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")  

        mqtt_client_name_entry = ctk.CTkEntry(self)
        mqtt_client_name_entry.grid(row=4, column=1, padx=10, pady=10, sticky="w") 

        mqtt_server_label = ctk.CTkLabel(self, text="MQTT Server:")
        mqtt_server_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")  

        mqtt_server_entry = ctk.CTkEntry(self)
        mqtt_server_entry.grid(row=5, column=1, padx=10, pady=10, sticky="w") 

        mqtt_port_label = ctk.CTkLabel(self, text="MQTT Port:")
        mqtt_port_label.grid(row=6, column=0, padx=10, pady=10, sticky="e")  

        # Entry field for MQTT port, restrict input to integers
        mqtt_port_entry = create_numeric_entry(self, 'int', data_length=4)
        mqtt_port_entry.grid(row=6, column=1, padx=10, pady=10, sticky="w") 

        receive_topic_label = ctk.CTkLabel(self, text="Receive Topic:")
        receive_topic_label.grid(row=7, column=0, padx=10, pady=10, sticky="e") 

        receive_topic_entry = ctk.CTkEntry(self)
        receive_topic_entry.grid(row=7, column=1, padx=10, pady=10, sticky="w")  

        send_topic_label = ctk.CTkLabel(self, text="Send Topic:")
        send_topic_label.grid(row=8, column=0, padx=10, pady=10, sticky="e")  

        send_topic_entry = ctk.CTkEntry(self)
        send_topic_entry.grid(row=8, column=1, padx=10, pady=10, sticky="w")  


        # Dropdown menu for device port selection
        dropdown_label = ctk.CTkLabel(self, text="Device Port:")
        dropdown_label.grid(row=9, column=0, padx=10, pady=10, sticky="e")  

        # Get the list of available ports and set the default value
        port_list = get_port_list()
        port_clicked = ctk.StringVar(value = port_list[0])

        # Dropdown menu to display available ports
        dropdown_menu = ctk.CTkOptionMenu(self, variable = port_clicked, values = port_list)
        dropdown_menu.grid(row=9, column=1, padx=10, pady=10, sticky="w")  

        # MODIFICAR MODEL_ENTRY
        self.model_entry.insert("1.0", "Texto insertado desde Page2")

        # Buttons for navigation and compiling/deploying   
        edit_config_btn = ctk.CTkButton(self, text="Edit Configuration", command=lambda: controller.show_frame(Page1))
        edit_config_btn.grid(row=10, column=0, padx=50, pady=10, sticky="ew")  

        compile_btn = ctk.CTkButton(self, text="Compile and Deploy", command=lambda: save_values_page2(controller, Page3, file_name_entry, ssid_entry, password_entry, ip_esp32_entry,
                                                                                                        mqtt_client_name_entry, mqtt_server_entry, mqtt_port_entry,
                                                                                                        receive_topic_entry, send_topic_entry, port_clicked, self.model_entry))
        
        compile_btn.grid(row=10, column=1, padx=50, pady=10, sticky="ew")


  
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
        back_button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(Page2))
        back_button.grid(row=1, column=0, padx=50, pady=10, sticky="ew")

        # Button to create model and proceed to next page 
        create_model_btn = ctk.CTkButton(self, text="Create Model", font=("helvetica",13),  command=lambda: (controller.show_frame(Page4), set_arduino_code(self.model_entry.get("1.0",'end-1c'))))
        create_model_btn.grid(row=1, column=1, padx=50, pady=10, sticky="ew")


    def get_model_entry(self):
        return self.model_entry


class Page4(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        for i in range(4): 
            self.grid_rowconfigure(i, weight=1)

        for i in range(3): 
            self.grid_columnconfigure(i, weight=1)

        # Creating console text area
        console_text = ScrolledText(self, bg="black", fg="white")
        console_text.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")  

        # Label to display selected training data file
        train_file_label = ctk.CTkLabel(self, text="No file chosen")
        train_file_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")

        # Button to open CSV file for training data
        open_train_dataset_btn = ctk.CTkButton(self, text="Open Training Data File", command=lambda: set_training_path(train_file_label, train_model_button))
        open_train_dataset_btn.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Label to display selected validation data file
        validation_file_label = ctk.CTkLabel(self, text="No file chosen")
        validation_file_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        # Button to open CSV file for validation data
        open_val_dataset_btn = ctk.CTkButton(self, text="Open Validation Data File", command=lambda: set_validation_path(validation_file_label, train_model_button))
        open_val_dataset_btn.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        # Button to navigate back to the previous page
        back_button = ctk.CTkButton(self, text="Back", command=lambda: controller.show_frame(Page3))
        back_button.grid(row=3, column=0, padx=30, pady=5, sticky="ew")  

        # Button to train the model
        train_model_button = ctk.CTkButton(self, text="Train model", command=lambda: train_async(console_text, upload_sketch_button))
        train_model_button.grid(row=3, column=1, padx=30, pady=5, sticky="ew")

        # Button to upload the sketch
        upload_sketch_button = ctk.CTkButton(self, text="Upload Sketch", command=lambda: create_sketch(console_text))
        upload_sketch_button.grid(row=3, column=2, padx=30, pady=5, sticky="ew")  

        # Disable train model button until model is trained
        train_model_button.configure(state='disabled')

        # Disable upload sketch button until model is trained
        upload_sketch_button.configure(state='disabled')

