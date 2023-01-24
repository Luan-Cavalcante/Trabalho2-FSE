import pid
import temp_ambiente
import gpio
from gpio import Gpio
from uart_modbus import InterfaceComando
import time
from forno import Forno
import log 

def main():
    data = temp_ambiente.sample_temp()
    my_gpio = Gpio()
    interface =  InterfaceComando()
    state = 0
    modo = True
    forno = Forno()

    while True:
        if state == 2:
            my_gpio.controle_temp()
        #comando = interface.le_comando_usuario()

        interface.envia_mensagem('0xC3')
        comando = interface.recebe_mensagem()

        # máquina de estadoooooo
        if comando == int('0xA1',16):
            # se comando for ligar
            # estado ligado.
            # que significa ligar o LED, e esperar o aquecimento.
            print('LIGA O SISTEMA DJOW')
            # enviar pro 
            #interface.liga_forno()
            interface.envia_mensagem('0xD3','0x01')

        elif comando == int('0xA2',16):
            # se comando for desligar 
            # estado desligado
            print('DESLIGA AÍ DJOW')
            interface.desliga_all()
            state = 0

        elif comando == int('0xA3',16):
            print('INICIOOOOUUU O PROCESSO')
            interface.envia_mensagem('0xD5','0x01')

            # Inicia o controle de temp
            state = 2

            my_gpio.controle_temp()
    
        elif comando == int('0xA4',16):
            # se comando for iniciar aquecimento e não tiver ligado, faz o quê ?
            # se comando for cancela processo, para tudo.
        
            print('CANCELA AÍ VEI')
            interface.envia_mensagem('0xD5','0x00')

        elif comando == int('0xA5',16):
            # se comando for altera processo 
            # muda aquecimento por referência, para aquecimento por curva
            modo = not modo
            codigo = '0x00' if modo else '0x01'
            
            print("Change CHAAAAANGEEEE")
            interface.envia_mensagem('0xD4',codigo)

        time.sleep(0.5)

if __name__ == '__main__':
    main()