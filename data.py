import pandas as pd
import numpy as np

# Función para crear los conjuntos de datos X--Y
def create_window_xy(df, window_size, target_window_size):
    X = []
    y = []
    dates = []

    for i in range(len(df) - window_size - target_window_size + 1):
        past_data = df.iloc[i:i+window_size]  # Datos pasados (ventana)
        target_data = df.iloc[i+window_size:i+window_size+target_window_size]['Avg Temp(Celsius)']  # Valores objetivo de temperatura

        target_date = df.index[i+window_size+target_window_size-1]  # Fecha correspondiente al último valor objetivo

        temp_humidity_pairs = past_data[['Avg Temp(Celsius)', 'Avg Humidity(%)']].values.tolist()
        X.append(temp_humidity_pairs)  # Añadir los datos pasados a X
        y.append(target_data.tolist())  # Añadir la lista de valores objetivo a y
        dates.append(target_date)  # Añadir la fecha correspondiente a dates

    dates = np.array(dates)
    X = np.array(X)
    y = np.array(y)

    return dates, X, y


def get_data():
    # Suponiendo que 'data' es tu DataFrame con las columnas 'Datetime',  'Avg Temp(Celsius), Avg Humidity(%) y Precipitation(mm)'
    dataset = pd.read_csv('MergedDataset.csv')

    #Set Datetime as index
    dataset['Datetime'] = pd.to_datetime(dataset['Datetime'])
    dataset.set_index(dataset['Datetime'], inplace=True)

    # Remove Datetime and Precipitation columns
    columns_to_drop = ['Datetime', 'Precipitation(mm)']
    dataset = dataset.drop(columns=columns_to_drop)

    data = dataset.loc['2021-01-01 00:30:00':]


    print(data.isna().sum())

    data = data.fillna(method='ffill')
    print(data.isna().sum())


    # Crear los conjuntos de datos 'trainX' y 'trainY' utilizando la función
    dates, X, y = create_window_xy(data, 24,24)


    # Calcular la longitud de cada conjunto
    total_rows = len(data)
    split1 = int(total_rows * 0.7)  # 70% para train
    split2 = int(total_rows * 0.2)  # 20% para validation
    split3 = total_rows - split1 - split2  # Lo que queda para test

    # Dividir el DataFrame en tres conjuntos
    dates_train, X_train, y_train = dates[:split1], X[:split1], y[:split1]
    dates_val, X_val, y_val = dates[split1:split1 + split2], X[split1:split1 + split2], y[split1:split1 + split2]
    dates_test, X_test, y_test = dates[split1 + split2:], X[split1 + split2:], y[split1 + split2:]

    print('X_train: \n', X_train)
    print('y_train: \n', y_train)


    # df_x_train = pd.DataFrame(X_train)
    # df_x_train.to_csv('X_train.csv', index=False)

    # df_y_train = pd.DataFrame(y_train)
    # df_y_train.to_csv('X_train.csv', index=False)

    np.savetxt('datos_x_entrenamiento.csv', X_train, delimiter=',')
    np.savetxt('datos_y_entrenamiento.csv', y_train, delimiter=',')


    return dates_train, X_train, y_train, dates_val, X_val, y_val, dates_test, X_test, y_test