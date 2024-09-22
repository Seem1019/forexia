import time
import random
import logging
import torch
from dotenv import load_dotenv
import os
from strategies.ema_strategy import calcular_ema
from iqoption.iqoption_handler import IQOptionHandler
from models.transformer_model import TimeSeriesTransformer
from models.data_preparation import preparar_datos
from utils.logging_config import configurar_logging

# Cargar las variables de entorno y configurar el logging
configurar_logging()
load_dotenv()
email = os.getenv('IQ_OPTION_EMAIL')
password = os.getenv('IQ_OPTION_PASSWORD')

# Parámetros del modelo Transformer
input_size = 4  # Precios de apertura, cierre, máximo, mínimo
d_model = 64
nhead = 4
num_encoder_layers = 2
dim_feedforward = 128
output_size = 1  # Predicción binaria: call o put

# Crear el modelo con la misma arquitectura utilizada en el entrenamiento
model = TimeSeriesTransformer(input_size=input_size, d_model=d_model, nhead=nhead,
                              num_encoder_layers=num_encoder_layers, dim_feedforward=dim_feedforward,
                              output_size=output_size)
model.load_state_dict(torch.load('models/transformer_model.pth'))
model.eval()  # Poner el modelo en modo de evaluación


def hacer_inferencia_transformer(velas, modelo):
    """
    Hace inferencias usando el modelo de transformer para decidir si hacer 'call' o 'put'.
    Ahora también incluye la tendencia con la EMA y compara el cierre con la última vela.
    :param velas: Las últimas velas recolectadas.
    :param modelo: El modelo Transformer entrenado.
    :return: 'call', 'put' o None si no se debe operar.
    """
    # Preparar los datos (secuencia de velas)
    X, close_prices = preparar_datos(velas, sequence_length=20)
    
    # Tomar la última secuencia de las velas recolectadas
    X_tensor = torch.tensor(X[-1:], dtype=torch.float32)  # Última secuencia
    
    # Calcular la EMA de las últimas 20 velas
    ema_actual = calcular_ema(close_prices, timeperiod=20)
    cierre_actual = velas[-1]['close']  # Último precio de cierre
    
    # Realizar la inferencia con el Transformer (logits)
    logits = modelo(X_tensor).item()  # Logits (valor sin aplicar sigmoide)
    
    # Aplicar sigmoide para convertir los logits en probabilidad
    probabilidad = torch.sigmoid(torch.tensor(logits)).item()

    print(f"Logits: {logits}, Probabilidad: {probabilidad}")
    
    # Decidir si la predicción está alineada con la tendencia (EMA)
    if cierre_actual > ema_actual:
        print("Tendencia alcista (precio por encima de la EMA)")
        probabilidad += 0.2  # Sumar peso si la predicción es alcista y la tendencia también
        print(f"Probabilidad ajustada ({probabilidad}) ")

    else:
        print("Tendencia bajista (precio por debajo de la EMA)")
        probabilidad -= 0.2  # Restar peso si la predicción es bajista y la tendencia es bajista
        print(f"Probabilidad ajustada ({probabilidad})")


    # Operar solo si la probabilidad ajustada es mayor al 70%
    if probabilidad >= 0.7:
        # Decisión basada en el valor de la probabilidad y el precio de cierre de la última vela
        if probabilidad > 0.7 and cierre_actual > velas[-2]['close']:
            return "call"  # Predicción de subida y precio de cierre es mayor que el anterior
        else:
            return "put"  # Predicción de bajada o precio de cierre es menor o igual al anterior
    else:
        print(f"Probabilidad ajustada ({probabilidad}) es menor al 70%. No se realizará operación.")
        return None  # No operar si la probabilidad ajustada es menor al 70%



def ciclo_de_operaciones_transformer(iq_handler, par, modelo):
    """
    Ciclo principal de operaciones usando el modelo Transformer para tomar decisiones de trading.
    :param iq_handler: Manejador de la API de IQ Option.
    :param par: Par de divisas a operar (ej. "EURUSD-OTC").
    :param modelo: El modelo Transformer entrenado para hacer inferencias.
    """
    while True:
        # Verificar si el par está disponible para operar
        if iq_handler.is_market_open(par):
            logging.info(f"{par} está disponible para operar.")

            # Obtener más de 20 velas (por ejemplo, 25) para generar secuencias de longitud 20
            velas = iq_handler.obtener_velas(par, 60, 25)

            # Imprimir cuántas velas se han obtenido
            print(f"Velas obtenidas: {len(velas)}")


            if len(velas) < 21:
                raise ValueError("No hay suficientes velas para crear una secuencia.")

            if velas:
                # Hacer inferencia con el Transformer y pasar el modelo como parámetro
                accion = hacer_inferencia_transformer(velas, modelo)
                
                if accion is not None:  # Solo operar si la probabilidad ajustada es mayor al 70%
                    monto = 1  # Monto de la operación en la moneda de la cuenta
                    duracion_segundos = 60  # Duración de la operación (1 minuto)

                    # Realizar la operación en IQ Option
                    resultado_operacion = iq_handler.realizar_operacion(par, monto, accion, duracion_segundos)
                    logging.info(f"Operación completada con resultado: {resultado_operacion}")
                else:
                    logging.info("Probabilidad ajustada menor al 70%, no se realiza operación.")

            # Esperar 60 segundos antes de la próxima operación
            time.sleep(60)
        else:
            logging.error(f"{par} no está disponible en este momento.")
            break



    """
    Ciclo principal de operaciones usando el modelo Transformer para tomar decisiones de trading.
    :param iq_handler: Manejador de la API de IQ Option.
    :param par: Par de divisas a operar (ej. "EURUSD-OTC").
    """
    while True:
        # Verificar si el par está disponible para operar
        if iq_handler.is_market_open(par):
            logging.info(f"{par} está disponible para operar.")

            # Obtener las últimas 20 velas (1 minuto cada una)
            velas = iq_handler.obtener_velas(par, 60, sequence_length)

            if velas:
                # Hacer inferencia con el Transformer para decidir la operación
                accion = hacer_inferencia_transformer(velas)
                monto = 1  # Monto de la operación en la moneda de la cuenta
                duracion_segundos = 60  # Duración de la operación (1 minuto)

                # Realizar la operación en IQ Option
                resultado_operacion = iq_handler.realizar_operacion(par, monto, accion, duracion_segundos)
                logging.info(f"Operación completada con resultado: {resultado_operacion}")

            # Esperar 60 segundos antes de la próxima operación
            time.sleep(60)
        else:
            logging.error(f"{par} no está disponible en este momento.")
            break


if __name__ == "__main__":
    # Crear el manejador de IQ Option con las credenciales
    iq_handler = IQOptionHandler(email, password)

    # Ejecutar el ciclo de operaciones para el par EURUSD-OTC
    ciclo_de_operaciones_transformer(iq_handler, "EURUSD-OTC",model)
