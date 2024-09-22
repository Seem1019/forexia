import numpy as np
import logging

def calcular_ema(close_prices, timeperiod=20):
    """Calcula la EMA (Media Móvil Exponencial) manualmente."""
    smoothing = 2 / (timeperiod + 1)
    ema_values = [np.mean(close_prices[:timeperiod])]  # Promedio inicial
    for price in close_prices[timeperiod:]:
        ema_actual = (price - ema_values[-1]) * smoothing + ema_values[-1]
        ema_values.append(ema_actual)
    return ema_values[-1]

def ejecutar_estrategia_ema(iq_handler, par):
    """Ejecuta la estrategia basada en EMA."""
    velas = iq_handler.obtener_velas(par, 60, 20)
    if velas:
        close_prices = np.array([vela['close'] for vela in velas])
        ema_20 = calcular_ema(close_prices)
        logging.info(f"EMA de 20 periodos calculada: {ema_20}")
        return ema_20
    return None
