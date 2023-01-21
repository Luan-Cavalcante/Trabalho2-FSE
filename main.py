import pid
import temp_ambiente
import gpio
from gpio import Gpio
from uart_modbus import InterfaceComando

def main():
    data = temp_ambiente.sample_temp()
    pid.pid_configura_constantes(30.0,0.2,400.0)
    pid.pid_atualiza_referencia(80.0)
    print(pid.pid_controle(35.0))
    my_gpio = Gpio(23,24)
    
    my_gpio.hello()

    interface = InterfaceComando()

    # main loop
    while True:
        # estado desligado
        comando = interface.le_comando_usuario()

        # se comando for ligar
            # estado ligado.
            # interface ligar.
            # que significa ligar o LED, e esperar o aquecimento.
        
        # se comando for desligar 
            # estado desligado

        # se comando for iniciar aquecimento e não tiver ligado, faz o quê ?

        # se comando for altera processo 
            # muda aquecimento por referência, para aquecimento por curva
        
        # se comando for cancela processo, para tudo.
        

        # estado ligado e sistema desligado
            # liga led e tals
        
        # estado ligado e sistema ligado

        time.sleep(0.5)


if __name__ == '__main__':
    main()