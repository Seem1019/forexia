import numpy as np

import numpy as np

def preparar_datos(velas, sequence_length):
    """
    Convierte una lista de velas en secuencias de datos con un tamaño específico (sequence_length).
    :param velas: Lista de diccionarios con las velas obtenidas (precios de apertura, cierre, volumen, etc.).
    :param sequence_length: Longitud de la secuencia de entrada que se le pasará al Transformer.
    :return: Arrays de características (X) y etiquetas (Y) para entrenar o hacer inferencias.
    """
    if len(velas) < sequence_length:
        raise ValueError("No hay suficientes velas para generar una secuencia.")
    
    # Convertimos las velas en arrays de características (input_size = 4 en este caso)
    close_prices = np.array([float(vela['close']) for vela in velas])
    open_prices = np.array([float(vela['open']) for vela in velas])
    high_prices = np.array([float(vela['max']) for vela in velas])  # Cambiado de 'high' a 'max'
    low_prices = np.array([float(vela['min']) for vela in velas])   # Cambiado de 'low' a 'min'

    # Stack de características
    features = np.stack([open_prices, high_prices, low_prices, close_prices], axis=1)

    # Imprimir las características generadas
    print("Características generadas (features)")


    # Crear secuencias de tamaño `sequence_length` para alimentar al modelo
    X, Y = [], []
    for i in range(len(features) - sequence_length):
        X.append(features[i:i+sequence_length])  # Secuencia de entrada
        # Etiqueta: 1 si el precio de cierre sube, 0 si baja
        label = 1 if close_prices[i + sequence_length] > close_prices[i + sequence_length - 1] else 0
        Y.append(label)

    # Verifica las dimensiones de X
    if len(X) == 0:
        raise ValueError("La secuencia generada está vacía.")
    
    print(f"Secuencias generadas: {len(X)}")

    return np.array(X), np.array(Y)
