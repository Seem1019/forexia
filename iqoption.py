from iqoptionapi.stable_api import IQ_Option
import time
import logging

# Configura el logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

# Conectar a la API de IQ Option
email = 'tu_correo@example.com'  # Reemplaza con tu email de IQ Option
password = 'tu_contraseña'  # Reemplaza con tu contraseña de IQ Option
api = IQ_Option(email, password)

# Intentar iniciar sesión
check, reason = api.connect()
if check:
    logging.info("Conectado exitosamente a IQ Option")
else:
    logging.error(f"Error al conectar: {reason}")
    exit(1)

# Asegúrate de estar conectado
api.change_balance("PRACTICE")  # O "REAL" para cuentas reales

# Función para recibir las velas en tiempo real
def obtener_velas_en_tiempo_real(par, intervalo, tiempo):
    logging.info(f"Solicitando velas de {par} en intervalos de {intervalo} segundos.")
    while True:
        velas = api.get_candles(par, intervalo, 1, tiempo)
        if velas:
            vela = velas[0]
            logging.info(f"Vela recibida: Tiempo: {vela['from']}, Apertura: {vela['open']}, Cierre: {vela['close']}")
        time.sleep(60)  # Esperar 60 segundos para la siguiente vela

# Par de divisas OTC para EUR/USD
par = 'eurusd-otc'

# Verificar si el par está disponible
if api.get_all_open_time()['digital'][par]['open']:
    logging.info(f"{par} está disponible para operar.")

    # Obtener tiempo actual del servidor
    tiempo_actual = time.time()

    # Solicitar velas de 1 minuto
    obtener_velas_en_tiempo_real(par, 60, tiempo_actual)
else:
    logging.error(f"{par} no está disponible en este momento.")

# Desconectar al finalizar
api.close()
