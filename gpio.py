import RPi.GPIO as GPIO
import time
from uart_modbus import InterfaceComando
import temp_ambiente
import pid
import os

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class Gpio(metaclass=SingletonMeta):
    def __init__(self) -> None:

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)

        # estudar PWM
        self.resistor = GPIO.PWM(23,1000)
        self.ventoinha = GPIO.PWM(24,1000)

        self.resistor.start(0)
        self.ventoinha.start(0)

        # interface de comando 
        self.interface = InterfaceComando()
        self.sinal_de_controle = 0.0
        self.referencia = 0.0
        self.Kp = 0.0  # Ganho Proporcional
        self.Ki = 0.0  # Ganho Integral
        self.Kd = 0.0  # Ganho Derivativo
        self.T = 1.0   # Período de Amostragem (ms)
        self.erro_total = 0.0
        self.erro_anterior = 0.0
        self.sinal_de_controle_MAX = 100.0
        self.sinal_de_controle_MIN = -100.0

    def pid_configura_constantes(self,Kp_, Ki_, Kd_):
        self.Kp = Kp_
        self.Ki = Ki_
        self.Kd = Kd_

    def pid_controle(self,saida_medida: float)-> float:
        erro = self.referencia - saida_medida
        print(self.referencia)
        print(f'error eh de {erro}')
        self.erro_total += erro

        if self.erro_total >= self.sinal_de_controle_MAX:
            self.erro_total = self.sinal_de_controle_MAX

        elif self.erro_total <= self.sinal_de_controle_MIN:
            self.erro_total = self.sinal_de_controle_MIN
            
        delta_error = erro - self.erro_anterior
        print(delta_error)

        self.sinal_de_controle = self.Kp*erro + (self.Ki*self.T)*self.erro_total + (self.Kd/self.T)*delta_error
        
        print(self.sinal_de_controle)

        if self.sinal_de_controle >= self.sinal_de_controle_MAX:
            self.sinal_de_controle = self.sinal_de_controle_MAX

        elif self.sinal_de_controle <= self.sinal_de_controle_MIN:
            self.sinal_de_controle = self.sinal_de_controle_MIN
        
        print(self.erro_anterior)
        self.erro_anterior = erro

        return self.sinal_de_controle

    def pid_atualiza_referencia(self,referencia_):
        self.referencia = referencia_

    def hello(self):
        print("Hello from singleton class")

    def esfria(self,duty : int) -> None:

        duty = abs(duty)

        if duty > 0 and duty < 40:
            duty = 40

        self.ventoinha.ChangeDutyCycle(duty)
        #print(f"Duty mudada para {duty}")
    
    def esquenta(self, duty:int) -> None:
        if duty < 0:
            print("Tem alguma coisa errada, duty negativo\n")
            return 

        self.resistor.ChangeDutyCycle(duty)
        #print(f"Duty mudada para {duty}")

    def controle_temp(self):
        # Lê temperatura interna
        self.interface.envia_mensagem('0xC1')
        time.sleep(0.5)
        temperatura_interna = self.interface.recebe_mensagem()

        # Lê temp referencia
        self.interface.envia_mensagem('0xC2')
        time.sleep(0.5)
        temperatura_ref = self.interface.recebe_mensagem()

        # Lê temp ambiente
        data = temp_ambiente.sample_temp()
        temperatura_ambiente = data.temperature

        # atualiza referência
        self.pid_atualiza_referencia(temperatura_ref)

        # pid controle
        sinal_controle = int(self.pid_controle(temperatura_interna))

        print(f"Temperatura referência : {temperatura_ref}\nTemperatura Interna : {temperatura_interna}\nSinal controle :{sinal_controle}")

        # atualiza pwm
        if sinal_controle > 0:
            self.esquenta(sinal_controle)
        else:    
            self.esfria(sinal_controle)
        
        print(f"sinal de controle : {sinal_controle}")
        self.interface.envia_sinal_controle(sinal_controle)