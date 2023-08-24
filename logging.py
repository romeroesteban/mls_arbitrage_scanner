import logging
import datetime

# Configurar el logger
logging.basicConfig(filename='registro3.log', filemode='a', level=logging.INFO)
# Escribir mensajes de registro

fecha_actual = datetime.datetime.now()

logging.info('### NUEVA EJECUCIÓN ### ' + str(fecha_actual))
