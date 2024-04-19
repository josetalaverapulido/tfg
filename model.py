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
from tensorflow.keras.callbacks import Callback

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

def set_cpp_code(new_value):
    global cpp_code
    cpp_code = new_value

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



class ProgressBarUpdater(Callback):
    def __init__(self, progress_bar, total_epochs, progress_bar_label):
        super(ProgressBarUpdater, self).__init__()
        self.progress_bar = progress_bar
        self.total_epochs = total_epochs
        self.progress_bar_label = progress_bar_label

    def on_epoch_end(self, epoch, logs=None):
        # Calculate current progress
        progress = (epoch + 1) / self.total_epochs * 100
        self.progress_bar['value'] = progress

        # If progress bar is complete, update label
        if progress == 100:
            self.progress_bar_label.configure(text="Model trained")





def train_async(console_text_widget, upload_sketch_button, progress_bar, progress_bar_label):
    # Redirect stdout to a buffer to capture model summary
    with StringIO() as buf, redirect_stdout(buf):
        model.summary()
        model_summary = buf.getvalue()

    # Clear console text widget and insert model summary
    console_text_widget.delete('1.0', 'end')
    console_text_widget.insert('1.0', model_summary)
    console_text_widget.update() 

    # Create a thread to execute training process
    train_thread = threading.Thread(target=train, args=(console_text_widget, upload_sketch_button, progress_bar, progress_bar_label))
    train_thread.start()


def train(console_text_widget, upload_sketch_button, progress_bar, progress_bar_label):
    global cpp_code

    # Modificar
    user_adam_learning_rate = float(get_adam_learning_rate())
    user_batch_size = int(get_batch_size())
    user_epochs = int(get_epochs())


    progress_bar['value'] = 0
    progress_bar.grid(row=3, column=1, padx=10, pady=10, sticky="ew")
    progress_bar.update_idletasks()

    progress_bar_label.configure(text="Training model...")
    progress_bar_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")  
    progress_bar_label.update_idletasks()

    # Compile the model
    model.compile(optimizer=Adam(learning_rate=user_adam_learning_rate), loss=MeanSquaredError(), metrics=['mean_absolute_error'])
    
    # Obtain data in this thread
    training_data_file_path = get_training_data_file_path()
    validation_data_file_path = get_validation_data_file_path()

    X_train, y_train = get_data(training_data_file_path)
    X_val, y_val = get_data(validation_data_file_path)

    try:
        console_text_widget.insert('end', "\nTraining model...")
        console_text_widget.update()  

        # Create the callback to update the progress bar
        progress_callback = ProgressBarUpdater(progress_bar, user_epochs, progress_bar_label)

        # Train the model with the newly obtained data
        history = model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=user_batch_size, epochs=user_epochs, callbacks=[progress_callback])

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
        set_cpp_code(cpp_code)
        print(cpp_code)

        upload_sketch_button.configure(state='normal')
    except ValueError:
        messagebox.showerror("Error", "Input data shape is not compatible with model expected shape")




