import pid
import temp_ambiente
import gpio
from gpio import Gpio

def init_system()->None:
    pid.pid_configura_constantes(30.0,0.2,400.0)
    pid.pid_atualiza_referencia(80.0)
    print(pid.pid_controle(35.0))
    my_gpio = Gpio(23,24)



def main():
    data = temp_ambiente.sample_temp()

    init_system()
    
    my_gpio.hello()

    # main loop
    while True:
        # estado desligado
        

        # estado ligado e sistema desligado
            # liga led e tals


        # estado ligado e sistema ligado



if __name__ == '__main__':
    main()