import pandas as pd

def cargar_velas_desde_csv(file_path):
    """
    Carga los datos históricos de velas desde un archivo CSV.
    :param file_path: Ruta al archivo CSV con los datos de velas.
    :return: Lista de diccionarios con las velas (cada diccionario tiene las características de la vela).
    """
    df = pd.read_csv(file_path)
    
    # Asumiendo que el archivo CSV tiene las columnas: 'open', 'high', 'low', 'close', 'volume'
    velas = df.to_dict('records')  # Convertir cada fila en un diccionario
    return velas
