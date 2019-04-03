import datetime
import time
import platform
import psutil
import netifaces
import os


class Sistema:

	def pegarSistema(self):
		resposta = 'Sistema: \n'
		resposta += 'OS: ' + platform.system() + ' - ' + platform.release() + '\n'
		resposta += 'Máquina: ' + platform.node() + ' - ' + platform.machine() + '\n'
		resposta += 'Uptime: ' + str(datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())) + '\n\n'
		resposta += self.pegarUptime() + '\n\n'

		resposta += 'Uso: \n'
		resposta += 'CPU: ' + str(psutil.cpu_percent()) + '%\n'
		resposta += 'RAM: ' + str(psutil.virtual_memory().percent) + '% de ' + str(round(psutil.virtual_memory().total / (10**9), 2)) + ' Giga \n'
		resposta += 'SWAP: ' + str(psutil.swap_memory().percent) + '% de ' + str(round(psutil.swap_memory().total / (10**9), 2)) + ' Giga \n'
		resposta += 'Discos: \n'
		resposta += self.pegarDiscosTexto() + '\n'

		resposta += 'Temperatura: \n'
		if ('armv7' in platform.machine()):
			res = os.popen('/opt/vc/bin/vcgencmd measure_temp').readline()
			resposta += 'CPU: ' + res.replace("temp=", "").replace("'C\n", " ºC")
		else:
			temps = psutil.sensors_temperatures()
			chaves = set(temps.keys())

			for chave in chaves:
				resposta += chave + '\n'
				if chave in temps:
					for entrada in temps[chave]:
						resposta += ((" %s: %s°C (pico=%s°C, crítica=%s°C) \n" % (
							entrada.label or chave, entrada.current, entrada.high, entrada.critical)))

		return resposta

	def pegarApp(self):
		resposta = 'Uso Vovô bot: \n'
		pid = os.getpid()
		processo = psutil.Process(pid)
		resposta += 'PID: ' + str(pid) + '\n'
		resposta += 'CPU: ' + str(processo.cpu_percent()) + '%\n'
		resposta += 'Memória: ' + str(round(processo.memory_percent(), 2)) + '% de ' + str(round(psutil.virtual_memory().total / (10**9), 2)) + ' Giga \n'
		resposta += 'Uptime: ' + str(datetime.datetime.now() - datetime.datetime.fromtimestamp(processo.create_time())) + '\n\n'

		return resposta

	def pegarCPUProcesso(self):
		pid = os.getpid()
		processo = psutil.Process(pid)
		perc = round(processo.cpu_percent(), 2)
		return perc

	def pegarMemoriaProcesso(self):
		pid = os.getpid()
		processo = psutil.Process(pid)
		perc = round(processo.memory_percent() / (10**6), 2)
		usage = round(((psutil.virtual_memory().total / (10**6)) * processo.memory_percent()) / 100, 2)
		return perc, usage

	def pegarCPU(self):
		perc = round(psutil.cpu_percent(), 2)
		return perc

	def pegarMemoria(self):
		perc = round(psutil.virtual_memory().percent, 2)
		usage = round(((psutil.virtual_memory().total / (10**6)) * psutil.virtual_memory().percent) / 100, 2)
		return perc, usage

	def pegarSwap(self):
		perc = round(psutil.swap_memory().percent, 2)
		usage = round(psutil.swap_memory().used / (10**6), 2)
		return perc, usage

	def pegarIPs(self):
		resposta = ''
		interfaces = netifaces.interfaces()
		for i in interfaces:
			if i == 'lo':
				continue
			iface = netifaces.ifaddresses(i).get(netifaces.AF_INET)
			if iface is not None:
				resposta = iface[0]['addr']
				#   for j in iface:
				# resposta += str(j['addr'])

		# resposta += 'Externo: ' + get('https://api.ipify.org').text
		return resposta

	def pegarDiscosTexto(self):
		resposta = ''
		#disk.device para pegar o nome mesmo /dev/sdaX
		for disk in psutil.disk_partitions(all=False):
		    resposta += str(disk.mountpoint) + ': ' + str(psutil.disk_usage(disk.mountpoint).percent) + '% de ' + str(round(psutil.disk_usage(disk.mountpoint).total / (10**9), 2)) + ' Gb \n'

		return resposta

	def pegarDiscos(self):
		resposta = []
		#disk.device para pegar o nome mesmo /dev/sdaX
		for disk in psutil.disk_partitions(all=False):
			resposta.append({disk.mountpoint: {"perc": psutil.disk_usage(disk.mountpoint).percent, "gb": round(psutil.disk_usage(disk.mountpoint).used / (10**9), 2)}})

		return resposta

	def pegarUptime(self):
		minute = 60
		hour = minute * 60
		day = hour * 24

		d = h = m = 0

		s = int(time.time()) - int(psutil.boot_time())

		d = s / day
		s -= d * day
		h = s / hour
		s -= h * hour
		m = s / minute
		s -= m * minute

		uptime = ""
		if d > 1:
			uptime = "%d dias, " % d
		elif d == 1:
			uptime = "1 dia, "

		return str(uptime + "%d:%02d:%02d" % (h, m, s))
