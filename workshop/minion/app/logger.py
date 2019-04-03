import json
import platform
import logging
import requests

from app.sistema import Sistema
from app import config


class Logger():
    def registrarHealth(self):
        try:
            print('healthing...')
            sistema = Sistema()
            memoria_perc, memoria_usada = sistema.pegarMemoria()
            swap_perc, swap_usada = sistema.pegarSwap()
            disco = sistema.pegarDiscos()
            hostname = platform.uname()[1]  # os.uname()[1]
            ip = sistema.pegarIPs()
            # timestamp = datetime.datetime.now().timestamp()
            url = config.url_konker_pub + config.usuarioKonker + "/health"
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            auth = (config.usuarioKonker, config.senhaKonker)

            # ## GERAL
            msg = {
                "id": config.dispositivoKonker,
                "health": 1,
                "host": {
                    "name": hostname,
                    "ip": ip,
                    "memory": {
                        "perc": memoria_perc,
                        "mb": memoria_usada
                    },
                    "cpu": sistema.pegarCPU(),
                    "swap": {
                        "perc": swap_perc,
                        "mb": swap_usada
                    },
                    "disks": disco
                }
            }
            requests.post(url, headers=headers, auth= auth, data=json.dumps(msg)).json()

            # resposta += self.pegarDiscos()

            logging.getLogger('minion.config').log(1, "health registrado na Konker")
            return True
        except Exception as e:
            print('erro: ' + str(e))
            return e

    def registrarExecucao(self, nome_operacao, duracao, mensagem, erro, codigo_erro):
        try:
            url = config.url_konker_pub + config.usuarioKonker + "/log"
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            auth = (config.usuarioKonker, config.senhaKonker)

            # ## GERAL
            if not erro:
                msg = {"action": nome_operacao, "status": 'sucess', "message": mensagem, "duration": duracao, }
            else:
                msg = {"action": nome_operacao, "status": 'failure', "message": str('error : ' + str(codigo_erro) + '-' + mensagem), }
            requests.post(url, headers=headers, auth= auth, data=json.dumps(msg)).json()
            # resposta += self.pegarDiscos()

            logging.getLogger('minion.config').log(1, "log registrado na Konker")
            return True
        except Exception as e:
            print('erro: ' + str(e))
            return e

    def registrarCiencia(self, nome_operacao):
        try:
            url = config.url_konker_pub + config.usuarioKonker + "/ack"
            headers = {'content-type': 'application/json', 'Accept': 'application/json'}
            auth = (config.usuarioKonker, config.senhaKonker)

            # ## GERAL
            msg = {'type': 'ack', "action": nome_operacao, }
            requests.post(url, headers=headers, auth= auth, data=json.dumps(msg)).json()

            # resposta += self.pegarDiscos()

            logging.getLogger('minion.config').log(1, "log de ciência de execução registrado na Konker")
            return True
        except Exception as e:
            print('erro: ' + str(e))
            return e
