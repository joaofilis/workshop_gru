import logging
import requests

from app.dispatcher import Dispatcher
from app import config


class Listener():
    __dispatcher = Dispatcher

    def __init__(self):
        print("   carregando listener...")
        self.__dispatcher = Dispatcher()

    def temComando(self):
        print('listening...')

        url = config.url_konker_sub + config.usuarioKonker + "/cmd"
        headers = {'content-type': 'application/json', 'Accept': 'application/json'}
        auth = (config.usuarioKonker, config.senhaKonker)
        comando = requests.get(url, headers=headers, auth= auth).json()

        if comando:
            # print('device', str(comando[0]['meta']['incoming']['deviceId']))
            if comando[0]['meta']['incoming']['deviceId'] == 'maestro' and \
                    comando[0]['meta']['outgoing']['channel'] == 'cmd':
                if comando[0]['data']['type'] == 'execution':
                    self.__dispatcher.executarComando(comando[0]['data']['action'])

        logging.getLogger('minion.config').log(1, "health registrado na Konker")
        return comando
