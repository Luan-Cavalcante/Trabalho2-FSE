from crc import calcula_CRC
import serial
from time import sleep

class InterfaceComando():
    def __init__(self) -> None:
        self.esp32_code = bytes([int('0x01',16)])
        self.matricula = bytes([int('1',16)]) + bytes([int('8',16)]) + bytes([int('3',16)]) + bytes([int('6',16)])
        self.codigo_solicita = bytes([int('0x23',16)])
        self.codigo_envia = bytes([int('0x16',16)])
        self.subcodigo_temp_interna = bytes([int('0xC1',16)])
        self.subcodigo_temp_ref = bytes([int('0xC2',16)])
        self.subcodigo_le_comando = bytes([int('0xC3',16)])
        self.subcodigo_sinal_controle = bytes([int('0xD1',16)])
        self.subcodigo_sinal_ref = bytes([int('0xD2',16)])
        self.subcodigo_estado_sys = bytes([int('0xD3',16)])
        self.subcodigo_modo_controle = bytes([int('0xD4',16)])
        self.subcodigo_estado_func = bytes([int('0xD5',16)])
        self.subcodigo_temp_ambiente = bytes([int('0xD6',16)])
        self.ser = serial.Serial ("/dev/ttyS0", 9600)

    def le_comando_usuario(self):
        mensagem = self.esp32_code + self.codigo_solicita + self.subcodigo_le_comando + self.matricula
        crc = calcula_CRC(mensagem)
        mensagem = mensagem + crc

        mensagem = self.recebe_mensagem()

        self.envia_mensagem(mensagem)
        sleep(0.03)

        mensagem = self.recebe_mensagem()
        
        ###
        ### Trata comando, para pegar essa parada
        ###

        return comando

    def monta_mensagem(self,codigo,subcodigo):
        mensagem = self.esp32_code + bytes([int(codigo,16)]) + bytes([int(subcodigo,16)]) + self.matricula
        crc = calcula_CRC(mensagem)
        mensagem = mensagem + crc
        print(len(mensagem))
        return mensagem

    def envia_mensagem(self,mensagem):
        #Open port with baud rate
        print(mensagem)
        self.ser.write(mensagem)
    
    def recebe_mensagem(self):
        mensagem = self.ser.read(9)
        if self.valida_mensagem_retorno(mensagem):
            print("Mensagem válida")
            print(mensagem)
            print(type(mensagem))
            return mensagem
        else:
            print("mensagem inválida")
            return 'erro'
        

    def valida_mensagem_retorno(self,mensagem) -> bool:
        if calcula_CRC(mensagem) == mensagem[-2:]:
            print("CRC funcionando")
            return True
        else:
            print("CRC bichado")
            return False

    def ligar(self):
        mensagem = self.monta_mensagem(self.codigo_envia,self.subcodigo_estado_sys)
        self.envia_mensagem(mensagem)
        

if __name__ == '__main__':
    i = InterfaceComando()
    i.envia_mensagem()
        