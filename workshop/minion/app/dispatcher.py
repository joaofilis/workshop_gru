import os
import logging
from app.logger import Logger


class Dispatcher():
    __logger = Logger

    def __init__(self):
        self.__logger = Logger()
        print("   carregando dispatcher...")

    def executarComando(self, acao):
        try:
            sucesso = True
            retorno = ''
            mensagem = ''
            duracao = 0  # deverá ser calculado para envio na mensagem de sucesso

            self.__logger.registrarCiencia(acao)
            if acao == 'executeJob69':
                print('execução do Job69')
                retorno = os.popen('sh Job69').readline()
            elif acao == 'reboot':
                print('reiniciando sistema')
                retorno = os.popen('sudo reboot').readline()
            elif acao == 'testeworkshop':
                print('Hello World Workshop')
                retorno = os.popen('ls').readline()
            # ########### registro de logs de execução, ignorar se o próprio serviço enviar estes logs
            # tratar as mensages de retorno para identificar se houve erro
            if retorno == [] or retorno != '':
                # registrar log de sucesso
                mensagem = 'sucesso'
                self.__logger.registrarExecucao(acao, duracao, mensagem, False, 0)
                logging.getLogger('minion.config').log(1, "ação " + acao + " executada com sucesso")
            else:
                # registrar log de erro
                codigo_erro = '0'
                mensagem = 'mensagem de erro'
                self.__logger.registrarExecucao(acao, 0, mensagem, True, codigo_erro)
                sucesso = False
                logging.getLogger('minion.config').log(1, "ação " + acao + " falhou. Erro " + str(codigo_erro) + ' - ' + mensagem)

            return sucesso
        except Exception as e:
            print('erro: ' + str(e))
            logging.getLogger('minion.config').log(1, " Erro " + str(e))
            return False
