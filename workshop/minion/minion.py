import time
import datetime
from app import config
from app.listener import Listener
from app.logger import Logger

tempoReiniciar = 30
__listener = Listener()
__logger = Logger()
__dataHoraHealth = datetime.datetime
__dataHoraListening = datetime.datetime

__dataHoraHealth = datetime.datetime.now() + datetime.timedelta(seconds = config.intervaloHelth)
__dataHoraListening = datetime.datetime.now() + datetime.timedelta(seconds = config.intervaloListening)
__listener.temComando()
__logger.registrarHealth()
try:
	pass
except Exception as e:
	print("Houve um erro ao iniciar o Minion. Reiniciando em %s segundos..." % str(tempoReiniciar))
	print("Erro %s" % e)
	time.sleep(tempoReiniciar)


# Keep the program running.
while 1:
	if (datetime.datetime.now() > __dataHoraHealth):
		config.carregar()
		__logger.registrarHealth()
		__dataHoraHealth = datetime.datetime.now() + datetime.timedelta(seconds = config.intervaloHelth)

	if (datetime.datetime.now() > __dataHoraListening):
		__listener.temComando()
		__dataHoraListening = datetime.datetime.now() + datetime.timedelta(seconds = config.intervaloListening)
	time.sleep(30)
