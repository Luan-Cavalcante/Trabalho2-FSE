from crc import calcula_CRC
import serial
from time import sleep
import struct

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
        
        return comando
    
    def desliga_all(self):
        self.envia_mensagem('0xD4','0x00')
        self.envia_mensagem('0xD5','0x00')
        self.envia_mensagem('0xD3','0x00')

    def envia_sinal_controle(self,valor:int):
        valor_int_em_bytes = struct.pack('<i',valor)
        print(valor_int_em_bytes)
        print(len(valor_int_em_bytes))

        mensagem = self.esp32_code + bytes([int('0x16',16)]) + bytes([int('0xD1',16)]) + self.matricula + valor_int_em_bytes
        
        crc = calcula_CRC(mensagem)

        mensagem = mensagem + crc

        self.ser.write(mensagem)


    def monta_mensagem(self,subcodigo,valor = ''):

        codigo = '0x23' if int(subcodigo,16) > 0xD0 else '0x16'

        if valor.strip():    
            mensagem = self.esp32_code + bytes([int(codigo,16)]) + bytes([int(subcodigo,16)]) + self.matricula + bytes([int(valor,16)])
        else:
            mensagem = self.esp32_code + bytes([int(codigo,16)]) + bytes([int(subcodigo,16)]) + self.matricula

        crc = calcula_CRC(mensagem)
        #print(type(mensagem[0]))
        #print(type(crc))
        #print(len(crc))
        mensagem = mensagem + crc
        #print(len(mensagem))
        return mensagem

    def envia_mensagem(self,subcodigo,valor = ''):
        mensagem = self.monta_mensagem(subcodigo,valor)

        self.ser.write(mensagem)
    
    def le_serial(self):
        for i in range(9):
            received_data = self.ser.read()              #read serial port
            sleep(0.03)
            data_left = self.ser.inWaiting()             #check for remaining byte
            received_data += self.ser.read(data_left)
            print(f'recebi {received_data}')
        
        return received_data

    def recebe_mensagem(self):

        mensagem = self.ser.read(9)

        if self.valida_mensagem_retorno(mensagem):
            numero = mensagem[3:len(mensagem)-2]

            if mensagem[2] < 195:
                #print("sou flooooat")
                floating_point_number = struct.unpack('<f', numero)[0]
                print(floating_point_number)

                return floating_point_number
            else:
                # interpreta como inteiro
                #print('sou inteeeirooooooo')
                integer = struct.unpack('<i', numero)[0]
                print(integer)
                return integer
        else:
            print("mensagem inválida")
            return 'erro'

    def mostra_mensagem(self,mensagem):
        for i in mensagem:
            print(i)

    def valida_mensagem_retorno(self,mensagem) -> bool:
        #print("Validando mensagem . . .")

        crc = calcula_CRC(mensagem[:-2])

        if crc == mensagem[-2:]:
            #print("CRC funcionando")
            return True
        else:
            #print("CRC bichado")
            return False

    def ligar(self):
        mensagem = self.monta_mensagem(self.codigo_envia,self.subcodigo_estado_sys)
        self.envia_mensagem(mensagem)

