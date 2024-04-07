import os
from tkinter import filedialog
from pathlib import Path
from tkinter import messagebox
import numpy as np

training_data_file_path = ""
validation_data_file_path = ""

training_data_ready = False
validation_data_ready = False

def set_training_data_file_path(new_value):
    global training_data_file_path
    training_data_file_path = new_value

def set_validation_data_file_path(new_value):
    global validation_data_file_path
    validation_data_file_path = new_value

def get_training_data_file_path():
    return training_data_file_path

def get_validation_data_file_path():
    return validation_data_file_path


def get_file_path(file_label):
    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Configure file types to only open CSV files
    filetypes = [("CSV files", "*.csv")]

    filepath = filedialog.askopenfilename(initialdir=current_directory, filetypes=filetypes)
    
    # Update the text of the text box
    if filepath:  
        file_label.config(text=os.path.basename(filepath))  
    else:  
        file_label.config(text="No file chosen")  
    
    filepath = Path(filepath)

    return filepath



def set_training_path(file_label, train_model_button):
    global training_data_ready, validation_data_ready

    filepath = get_file_path(file_label)
    set_training_data_file_path(filepath)

    training_data_ready = True
    if training_data_ready and validation_data_ready:
        train_model_button.config(state='normal')


def set_validation_path(file_label, train_model_button):
    global training_data_ready, validation_data_ready

    filepath = get_file_path(file_label)
    set_validation_data_file_path(filepath)

    validation_data_ready = True
    if training_data_ready and validation_data_ready:
        train_model_button.config(state='normal')


def get_data(filepath):
    x = []
    y = []

    with open(filepath, 'r') as file:
        lines = file.readlines()

        # Extract column names
        column_names = lines[0].strip().split(',')
        column_names = [col.lower() for col in column_names]

    try:
        # Verify if all column names start with 'x' or 'y'
        if not all(col.startswith('x') or col.startswith('y') for col in column_names):
            raise ValueError("Error! At least one value in column_names does not begin with 'x' or 'y' ")

        # Count the number of 'x' and 'y' columns
        count_x = sum(1 for col in column_names if col.startswith('x'))
        count_y = sum(1 for col in column_names if col.startswith('y'))

        # Process lines from the file, skipping the first line
        for line in lines[1:]:
            values = line.strip().split(',')
            y.append([float(val) for val in values[0:count_y]])
            x.append([float(val) for val in values[count_y:]])

    except ValueError as e:
        messagebox.showerror("Error", str(e) + "in " + str(filepath))

    return np.array(x), np.array(y)

