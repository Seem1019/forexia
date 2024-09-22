import logging
import time
from iqoptionapi.stable_api import IQ_Option

class IQOptionHandler:
    def __init__(self, email, password, balance_type="PRACTICE"):
        self.api = IQ_Option(email, password)
        self.connect()
        self.api.change_balance(balance_type)

    def connect(self):
        check, reason = self.api.connect()
        if check:
            logging.info("Conectado exitosamente a IQ Option")
        else:
            logging.error(f"Error al conectar: {reason}")
            exit(1)

    def is_market_open(self, par):
        return self.api.get_all_open_time()['digital'][par]['open']

    def obtener_velas(self, par, intervalo, cantidad):
        logging.info(f"Obteniendo {cantidad} velas de {par} con intervalo de {intervalo} segundos.")
        return self.api.get_candles(par, intervalo, cantidad, time.time())

    def realizar_operacion(self, par, monto, accion, duracion_segundos):
        logging.info(f"Realizando operación en {par}: Acción: {accion}, Monto: {monto}, Duración: {duracion_segundos} segundos.")
        _, id_operacion = self.api.buy_digital_spot(par, monto, accion, duracion_segundos // 60)

        while True:
            check, resultado = self.api.check_win_digital_v2(id_operacion)
            if check:
                logging.info(f"Resultado de la operación: {resultado}")
                break
        return resultado
