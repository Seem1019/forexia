import time
import logging
import random
from dotenv import load_dotenv
import os
from iqoption.iqoption_handler import IQOptionHandler
from strategies.ema_strategy import ejecutar_estrategia_ema
from utils.logging_config import configurar_logging

# Configurar el logging
configurar_logging()

# Cargar las variables de entorno
load_dotenv()
email = os.getenv('IQ_OPTION_EMAIL')
password = os.getenv('IQ_OPTION_PASSWORD')

def main():
    # Inicializar la API
    iq_handler = IQOptionHandler(email, password)

    par = "EURUSD-OTC"
    while True:
        # Verificar si el par está disponible
        if iq_handler.is_market_open(par):
            logging.info(f"{par} está disponible para operar.")
            ema_20 = ejecutar_estrategia_ema(iq_handler, par)

            # Decidir si hacer 'call' o 'put' basado en alguna lógica (por ahora aleatorio)
            accion = random.choice(["call", "put"])
            monto = 1
            duracion_segundos = 60

            if ema_20 is not None:
                iq_handler.realizar_operacion(par, monto, accion, duracion_segundos)

            # Esperar 60 segundos antes de la próxima operación
            time.sleep(60)
        else:
            logging.error(f"{par} no está disponible en este momento.")
            break

if __name__ == "__main__":
    main()
