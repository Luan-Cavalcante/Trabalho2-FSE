import pid
import temp_ambiente
import gpio
from gpio import Gpio

def main():
    pid.pid_configura_constantes(30.0,0.2,400.0)
    pid.pid_atualiza_referencia(80.0)

    print(pid.pid_controle(35.0))

    data = temp_ambiente.sample_temp()

    print(data.temperature)
    my_gpio = Gpio(23,24)

    if pid.pid_controle(35.0) > 40:
        print('aí muda carai')
    
    my_gpio.hello()

if __name__ == '__main__':
    main()