import tensorflow as tf
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import Adam
from keras.losses import MeanSquaredError
from contextlib import redirect_stdout
from io import StringIO
from data import get_data, get_training_data_file_path, get_validation_data_file_path
from everywhereml.code_generators.tensorflow import tf_porter
import threading
from tkinter import messagebox

model = None
batch_size = ""
epochs = ""
adam_learning_rate = ""
cpp_code = ""





def set_model(model_str):
    global model
    exec(model_str, globals())

def set_batch_size(new_value):
    global batch_size
    batch_size = new_value

def set_epochs(new_value):
    global epochs
    epochs = new_value

def set_adam_learning_rate(new_value):
    global adam_learning_rate
    adam_learning_rate = new_value

def get_model():
    return model

def get_batch_size():
    return batch_size

def get_epochs():
    return epochs

def get_adam_learning_rate():
    return adam_learning_rate

def get_cpp_code():
    return cpp_code





def train_async(console_text_widget, upload_sketch_button):
    # Redirect stdout to a buffer to capture model summary
    with StringIO() as buf, redirect_stdout(buf):
        model.summary()
        model_summary = buf.getvalue()

    # Clear console text widget and insert model summary
    console_text_widget.delete('1.0', 'end')
    console_text_widget.insert('1.0', model_summary)

    # Display compilation and training message
    console_text_widget.insert('end', "\nCompiling and training model...")
    console_text_widget.update()  # Update GUI to display message

    # Create a thread to execute training process
    train_thread = threading.Thread(target=train, args=(console_text_widget, upload_sketch_button))
    train_thread.start()


def train(console_text_widget, upload_sketch_button):
    # Global variable declaration
    global cpp_code

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=0.0001), loss=MeanSquaredError(), metrics=['mean_absolute_error'])
    
    # Obtain data in this thread
    training_data_file_path = get_training_data_file_path()
    validation_data_file_path = get_validation_data_file_path()

    X_train, y_train = get_data(training_data_file_path)
    X_val, y_val = get_data(validation_data_file_path)

    try:
        # Train the model with the newly obtained data
        history = model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=16, epochs=1)

        # Get the last value of each training metric
        last_train_loss = history.history['loss'][-1]
        last_train_mean_absolute_error = history.history['mean_absolute_error'][-1]

        # Get the last value of each validation metric
        last_val_loss = history.history['val_loss'][-1]
        last_val_mean_absolute_error = history.history['val_mean_absolute_error'][-1]

        # Print the last values of the metrics
        console_text_widget.insert('end', "\nTRAIN LOSS: {}\n".format(last_train_loss))
        console_text_widget.insert('end', "MEAN ABSOLUTE ERROR: {}\n".format(last_train_mean_absolute_error))
        console_text_widget.insert('end', "VALIDATION ERROR: {}\n".format(last_val_loss))
        console_text_widget.insert('end', "MEAN ABSOLUTE ERROR: {}\n".format(last_val_mean_absolute_error))

        # Convert the model to C++
        porter = tf_porter(model, X_train, y_train)
        cpp_code = porter.to_cpp(instance_name='model', arena_size=4096)
        print(cpp_code)

        upload_sketch_button.config(state='normal')
    except ValueError:
        messagebox.showerror("Error", "Input data shape is not compatible with model expected shape")


