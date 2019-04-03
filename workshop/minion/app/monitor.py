import datetime
from app.logger import Logger
from app import config


class Monitor:
    __ultimaMonitoracao = datetime.datetime
    __tolerancia = 0
    __logging = Logger()

    def __init__(self):
        print("   carregando monitor...")
        self.__ultimaMonitoracao = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(seconds = int(config.intervaloMonitoracao))
        print("   iniciando monitoração...")

    def monitorar(self):
        try:
            #print(str(datetime.datetime.now()) + " - Monitorando...")
            datahora = datetime.datetime.now().replace(microsecond=0) - datetime.timedelta(seconds = int(config.intervaloMonitoracao))

            if (datahora >= self.__ultimaMonitoracao):
                print('monitorando: ', datetime.datetime.now().replace(microsecond=0))

                log = self.__logging.registrarLogHelth('health')

                if not log:
                    print('houve um erro ao registrar log: ' + str(log))

                self.__ultimaMonitoracao = datetime.datetime.now().replace(microsecond=0)
        except Exception as e:
            print(str(datetime.datetime.now().replace(microsecond=0)) + " - Houve um problema durante a monitoração:  \n%s" % str(e))

        return ""
