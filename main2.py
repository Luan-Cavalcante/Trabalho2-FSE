import temp_ambiente
from Pid import PID
from uart_modbus import InterfaceComando
import time
from forno import Forno

def main():
    my_gpio = Gpio()
    interface =  InterfaceComando()
    forno = Forno()

    while True:
        comando = interface.le_comando_usuario()

        if forno.estado:
            if forno.funcionando:
                print('---- Forno ligado -----')
                forno.atualiza_temp_interna()
                forno.atualiza_temp_ref()
                forno.atualiza_temp_ambiente()
                forno.controle_temp()

            if comando == int('0xA2',16):
                # se comando for desligar 
                # estado desligado
                forno.desliga()

            elif comando == int('0xA3',16):
                print('INICIOOOOUUU O PROCESSO')
                forno.inicia_processo()

            elif comando == int('0xA4',16):
                # se comando for iniciar aquecimento e não tiver ligado, faz o quê ?
                # se comando for cancela processo, para tudo.
                forno.cancela_processo()

            elif comando == int('0xA5',16):
                # se comando for altera processo 
                # muda aquecimento por referência, para aquecimento por curva
                forno.change_mode()
            
            
        else:
            if comando == int('0xA1',16):
                # se comando for ligar
                forno.liga_forno()

        time.sleep(0.5)