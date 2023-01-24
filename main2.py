from uart_modbus import InterfaceComando
import time
from forno import Forno
import log 

def main():
    interface =  InterfaceComando()
    forno = Forno()
    forno.desliga()

    while True:
        comando = interface.le_comando_usuario()
        print(comando)
        if forno.estado:
            if forno.funcionando:
                print('---- Forno ligado -----')
                forno.atualiza_temp_interna()
                forno.atualiza_temp_ref()
                forno.atualiza_temp_ambiente()
                forno.show()
                if forno.modo:
                    forno.controle_temp()
                else:
                    forno.curva()

            if comando == int('0xA2',16):
                print('DESLIGAAA')
                # se comando for desligar 
                # estado desligado
                forno.desliga()

            elif comando == int('0xA3',16):
                print('INICIOOOOUUU O PROCESSO')
                forno.inicia_processo()

            elif comando == int('0xA4',16):
                print("CAAANCEELAAA")
                # se comando for iniciar aquecimento e não tiver ligado, faz o quê ?
                # se comando for cancela processo, para tudo.
                forno.cancela_processo()

            elif comando == int('0xA5',16):
                print("CHANGE MODE")
                # se comando for altera processo 
                # muda aquecimento por referência, para aquecimento por curva
                forno.change_mode()
            
        else:
            if comando == int('0xA1',16):
                # se comando for ligar
                forno.liga()

        mensagem = f'{forno.temp_interna},{forno.temp_ambiente},{forno.temp_referencia},{forno.pid_value}'
        log(mensagem)
        time.sleep(0.5)

if __name__ == "__main__":
    main()