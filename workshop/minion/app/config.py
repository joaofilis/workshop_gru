import os
import logging


class Config:

	__usuarioKonker = ''
	__senhaKonker = ''
	__url_konker_pub = ''
	__url_konker_sub = ''
	__intervaloListening = 0
	__intervaloHelth = 0

	def __init__(self):
		print("criando o config...")
		self.carregar()

	def __del__(self):
		pass

	def carregar(self):
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		LOCAL_SETTINGS_FILE = os.path.join(BASE_DIR, 'app/local', 'settings.py')

		try:
			with open(LOCAL_SETTINGS_FILE) as io:
				exec(compile(io.read(None), LOCAL_SETTINGS_FILE, 'exec'), locals())

			self.__usuarioKonker = locals()['usuarioKonker']
			self.__senhaKonker = locals()['senhaKonker']
			self.__url_konker_pub = locals()['url_konker_pub']
			self.__url_konker_sub = locals()['url_konker_sub']
			self.__intervaloListening = locals()['intervaloListening']
			self.__intervaloHelth = locals()['intervaloHelth']
			self.__dispositivoKonker = locals()['dispositivoKonker']
		except:
			logging.getLogger('minion.config').error("failed to load local/config.py")
			raise

	@property
	def usuarioKonker(self):
		return self.__usuarioKonker

	@property
	def senhaKonker(self):
		return self.__senhaKonker

	@property
	def intervaloListening(self):
		return self.__intervaloListening

	@property
	def intervaloHelth(self):
		return self.__intervaloHelth

	@property
	def url_konker_pub(self):
		return self.__url_konker_pub

	@property
	def url_konker_sub(self):
		return self.__url_konker_sub

	@property
	def dispositivoKonker(self):
		return self.__dispositivoKonker
