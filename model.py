# model.py
from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout
from keras.optimizers import Adam
from keras.losses import MeanSquaredError
from contextlib import redirect_stdout
from io import StringIO
from data import get_data
from everywhereml.code_generators.tensorflow import tf_porter
import threading

model = None
batch_size = ""
epochs = ""
adam_learning_rate = ""
cpp_code = ""





# Función para actualizar file_directory
def set_model(model_str):
    global model
    exec(model_str, globals())

# Función para actualizar file_directory
def set_batch_size(new_value):
    global batch_size
    batch_size = new_value

    # Función para actualizar file_directory
def set_epochs(new_value):
    global epochs
    epochs = new_value

    # Función para actualizar file_directory
def set_adam_learning_rate(new_value):
    global adam_learning_rate
    adam_learning_rate = new_value


# Función para obtener model
def get_model():
    return model

# Función para obtener batch_size
def get_batch_size():
    return batch_size

# Función para obtener epochs
def get_epochs():
    return epochs

# Función para obtener adam_learning_rate
def get_adam_learning_rate():
    return adam_learning_rate

# Función para obtener cpp_code
def get_cpp_code():
    return cpp_code





# Definir la función train
def train_async(console_text_widget, upload_sketch_button):
    with StringIO() as buf, redirect_stdout(buf):
        # Obtener el resumen del modelo como una cadena
        model.summary()
        model_summary = buf.getvalue()

    console_text_widget.delete('1.0', 'end')
    console_text_widget.insert('1.0', model_summary)

    # Eliminar y mostrar mensaje de compilación
    console_text_widget.insert('end', "\nCompiling and training model...")
    console_text_widget.update()  # Actualizar la interfaz gráfica para mostrar el mensaje


    # Crear un hilo para ejecutar train()
    train_thread = threading.Thread(target=train, args=(console_text_widget, upload_sketch_button))
    train_thread.start()

# Definir la función train en el hilo secundario
def train(console_text_widget, upload_sketch_button):
    global cpp_code

    # Compilar el modelo
    model.compile(optimizer=Adam(learning_rate=0.0001), loss=MeanSquaredError(), metrics=['mean_absolute_error'])
    
    # Obtener los datos en este hilo
    dates_train, X_train, y_train, dates_val, X_val, y_val, dates_test, X_test, y_test = get_data()

    # Entrenar el modelo con los datos recién obtenidos
    history = model.fit(X_train, y_train, validation_data=(X_val, y_val), batch_size=16, epochs=1)





    # Obtener el último valor de cada métrica de entrenamiento
    last_train_loss = history.history['loss'][-1]
    last_train_mean_absolute_error = history.history['mean_absolute_error'][-1]

    # Obtener el último valor de cada métrica de validación
    last_val_loss = history.history['val_loss'][-1]
    last_val_mean_absolute_error = history.history['val_mean_absolute_error'][-1]

    # Imprimir los últimos valores de las métricas
    console_text_widget.insert('end', "\nTRAIN LOSS: {}\n".format(last_train_loss))
    console_text_widget.insert('end', "MEAN ABSOLUTE ERROR: {}\n".format(last_train_mean_absolute_error))
    console_text_widget.insert('end', "VALIDATION ERROR: {}\n".format(last_val_loss))
    console_text_widget.insert('end', "MEAN ABSOLUTE ERROR: {}\n".format(last_val_mean_absolute_error))

    # Convertir el modelo a C++
    porter = tf_porter(model, X_train, y_train)
    cpp_code = porter.to_cpp(instance_name='model', arena_size=4096)

    upload_sketch_button.config(state='normal')