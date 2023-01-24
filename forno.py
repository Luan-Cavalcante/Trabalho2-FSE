from uart_modbus import InterfaceComando
import pandas as pd
from Pid import PID
import RPi.GPIO as GPIO
import time
import temp_ambiente


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


class Forno(metaclass=SingletonMeta):
    def __init__(self):

        self.estado = False
        self.temp_interna = 0
        self.temp_referencia = 0
        self.temp_ambiente = 0
        self.funcionando = False
        self.interface = InterfaceComando()
        self.modo = True
        self.pid_value = 0
        self.PID = PID()

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(24, GPIO.OUT)

        self.resistor = GPIO.PWM(23,1000)
        self.ventoinha = GPIO.PWM(24,1000)

        self.resistor.start(0)
        self.ventoinha.start(0)

    def liga(self):
        self.interface.liga_forno()
        self.estado = True
    
    def desliga(self):
        self.interface.desliga_all()
        self.estado = False
        self.pid_value = 0
        self.modo = True
    
    def funcionando(self):
        return self.funcionando
    
    def inicia_processo(self):
        self.interface.envia_mensagem('0xD5','0x01')
        self.funcionando = True

    def cancela_processo(self):
        self.interface.envia_mensagem('0xD5','0x00')
        self.funcionando = False
    
    def atualiza_temps(self,interna,referencia,ambiente):
        self.temp_interna = interna
        self.temp_referencia = referencia
        self.temp_ambiente = ambiente

    def change_mode(self):
        self.modo = not self.modo
        codigo = '0x00' if modo else '0x01'
        self.interface.envia_mensagem('0xD4',codigo)

    def esfria(self,duty : int) -> None:
        duty = abs(duty)
        if duty > 0 and duty < 40:
            duty = 40

        self.ventoinha.ChangeDutyCycle(duty)
    
    def esquenta(self, duty:int) -> None:
        if duty < 0:
            print("Tem alguma coisa errada, duty negativo\n")
            return 

        self.resistor.ChangeDutyCycle(duty)
    
    def atualiza_temp_ref(self):
        self.interface.envia_mensagem('0xC2')
        time.sleep(0.5)
        temperatura_ref = self.interface.recebe_mensagem()
        self.temp_referencia = temperatura_ref

    def atualiza_temp_ambiente(self):
        # Lê temp ambiente
        data = temp_ambiente.sample_temp()
        self.temp_ambiente = data.temperature

    def show(self):
        print(f"Temperatura Interna : {self.temp_interna}")
        print(f"Temperatura Referência : {self.temp_referencia}")
        print(f"Temperatura Ambiente : {self.temp_ambiente}")

    def atualiza_temp_interna(self):
        self.interface.envia_mensagem('0xC1')
        time.sleep(0.5)
        temperatura_interna = self.interface.recebe_mensagem()
        self.temp_interna = temperatura_interna

    def controle_temp(self):
        # Lê temperatura interna
        temp_interna = self.temp_interna
        temp_referencia = self.temp_referencia
        temp_ambiente = self.temp_ambiente
        
        # atualiza referência
        self.PID.pid_atualiza_referencia(temp_referencia)

        # pid controle
        sinal_controle = int(self.PID.pid_controle(temp_interna))
        self.pid_value = sinal_controle
        print(f"Temperatura referência : {temp_referencia}\nTemperatura Interna : {temp_interna}\nSinal controle :{sinal_controle}")

        if sinal_controle > 0:
            self.esquenta(sinal_controle)
        else:    
            self.esfria(sinal_controle)
        
        print(f"sinal de controle : {sinal_controle}")

        self.interface.envia_sinal_controle(sinal_controle)

    def curva(self):
        curva = pd.read_csv('curva_reflow.csv')
        times = list(curva['Tempo'])
        temperaturas = list(curva['Temperatura'])

        print(times,temperaturas)
        while True:


    