import re

def corregir_datos(archivo_entrada, archivo_salida):
    with open(archivo_entrada, 'r') as entrada, open(archivo_salida, 'w') as salida:
        for linea in entrada:
            linea = linea.strip()
            if ',' in linea:
                # Separar la fecha y el resto de la línea
                fecha, resto_linea = linea.split(',', 1)
                # Eliminar todas las comas del resto de la línea
                resto_linea = resto_linea.replace(',', '')
                numeros = []
                index = 0
                longitud = len(resto_linea)
                while index <= longitud - 6:
                    # Verificar si hay un número en la posición actual
                    if resto_linea[index] == '1' and resto_linea[index+1] == '.':
                        # Extraer el número de 6 caracteres
                        num = resto_linea[index:index+6]
                        numeros.append(num)
                        index += 6  # Avanzar 6 posiciones
                    else:
                        index += 1  # Avanzar una posición y seguir buscando
                # Reconstruir la línea corregida
                linea_corregida = fecha + ',' + ','.join(numeros)
                salida.write(linea_corregida + '\n')
            else:
                # Si no hay coma, se asume que es una línea incorrecta y se escribe tal cual
                salida.write(linea + '\n')


# Uso del script
corregir_datos('data/historical_candles.csv', 'datos_corregidos.csv')
