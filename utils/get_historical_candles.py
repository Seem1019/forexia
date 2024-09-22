import csv
import time
import os
from iqoptionapi.stable_api import IQ_Option
from dotenv import load_dotenv

# Cargar las credenciales desde las variables de entorno
load_dotenv()
email = os.getenv('IQ_OPTION_EMAIL')
password = os.getenv('IQ_OPTION_PASSWORD')

def obtener_historico_velas(iq_api, par, intervalo, cantidad, archivo_salida):
    """
    Obtiene el histórico de velas de un par de divisas y las guarda en un archivo CSV.
    Solo guarda los datos de apertura, cierre, máximo y mínimo.
    :param iq_api: La instancia de la API de IQ Option.
    :param par: El par de divisas (ej: 'EURUSD-OTC').
    :param intervalo: Intervalo de las velas en segundos (ej: 60 para 1 minuto).
    :param cantidad: Cantidad de velas a obtener.
    :param archivo_salida: Ruta del archivo CSV de salida.
    """
    # Obtener el timestamp actual (en segundos)
    tiempo_actual = int(time.time())
    
    # Obtener las velas desde la API
    velas = iq_api.get_candles(par, intervalo, cantidad, tiempo_actual)
    
    # Escribir las velas en un archivo CSV, con solo apertura, cierre, mínimo y máximo
    with open(archivo_salida, mode='w', newline='') as archivo_csv:
        escritor_csv = csv.writer(archivo_csv)
        escritor_csv.writerow(['open', 'close', 'min', 'max'])  # Encabezados del CSV
        
        for vela in velas:
            escritor_csv.writerow([vela['open'], vela['close'], vela['min'], vela['max']])

    print(f"Histórico de velas guardado en {archivo_salida}")

# Conectar a la API de IQ Option
iq_api = IQ_Option(email, password)

# Conectar y cambiar a cuenta de práctica
check, reason = iq_api.connect()
if not check:
    print(f"Error al conectar: {reason}")
    exit(1)

iq_api.change_balance("PRACTICE")  # Cambia a "REAL" para cuentas reales

# Obtener el histórico de velas
par = "EURUSD-OTC"
intervalo = 60  # Intervalo de 1 minuto
cantidad = 100000 # Cantidad máxima de velas a obtener (ajusta según lo que permita la API)
archivo_salida = "historico_velas.csv"

# Llamar a la función para obtener las velas históricas
obtener_historico_velas(iq_api, par, intervalo, cantidad, archivo_salida)
