#include <stdio.h>
#include <unistd.h> //Usado para a UART
#include <fcntl.h> //Usado para a UART
#include <termios.h> //Usado para a UART
#include <string.h>

short CRC16(short crc, unsigned char data)
{
    const short tbl[256] = {
        0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
        0xC601, 0x06C0, 0x0780, 0xC741, 0x0500, 0xC5C1, 0xC481, 0x0440,
        0xCC01, 0x0CC0, 0x0D80, 0xCD41, 0x0F00, 0xCFC1, 0xCE81, 0x0E40,
        0x0A00, 0xCAC1, 0xCB81, 0x0B40, 0xC901, 0x09C0, 0x0880, 0xC841,
        0xD801, 0x18C0, 0x1980, 0xD941, 0x1B00, 0xDBC1, 0xDA81, 0x1A40,
        0x1E00, 0xDEC1, 0xDF81, 0x1F40, 0xDD01, 0x1DC0, 0x1C80, 0xDC41,
        0x1400, 0xD4C1, 0xD581, 0x1540, 0xD701, 0x17C0, 0x1680, 0xD641,
        0xD201, 0x12C0, 0x1380, 0xD341, 0x1100, 0xD1C1, 0xD081, 0x1040,
        0xF001, 0x30C0, 0x3180, 0xF141, 0x3300, 0xF3C1, 0xF281, 0x3240,
        0x3600, 0xF6C1, 0xF781, 0x3740, 0xF501, 0x35C0, 0x3480, 0xF441,
        0x3C00, 0xFCC1, 0xFD81, 0x3D40, 0xFF01, 0x3FC0, 0x3E80, 0xFE41,
        0xFA01, 0x3AC0, 0x3B80, 0xFB41, 0x3900, 0xF9C1, 0xF881, 0x3840,
        0x2800, 0xE8C1, 0xE981, 0x2940, 0xEB01, 0x2BC0, 0x2A80, 0xEA41,
        0xEE01, 0x2EC0, 0x2F80, 0xEF41, 0x2D00, 0xEDC1, 0xEC81, 0x2C40,
        0xE401, 0x24C0, 0x2580, 0xE541, 0x2700, 0xE7C1, 0xE681, 0x2640,
        0x2200, 0xE2C1, 0xE381, 0x2340, 0xE101, 0x21C0, 0x2080, 0xE041,
        0xA001, 0x60C0, 0x6180, 0xA141, 0x6300, 0xA3C1, 0xA281, 0x6240,
        0x6600, 0xA6C1, 0xA781, 0x6740, 0xA501, 0x65C0, 0x6480, 0xA441,
        0x6C00, 0xACC1, 0xAD81, 0x6D40, 0xAF01, 0x6FC0, 0x6E80, 0xAE41,
        0xAA01, 0x6AC0, 0x6B80, 0xAB41, 0x6900, 0xA9C1, 0xA881, 0x6840,
        0x7800, 0xB8C1, 0xB981, 0x7940, 0xBB01, 0x7BC0, 0x7A80, 0xBA41,
        0xBE01, 0x7EC0, 0x7F80, 0xBF41, 0x7D00, 0xBDC1, 0xBC81, 0x7C40,
        0xB401, 0x74C0, 0x7580, 0xB541, 0x7700, 0xB7C1, 0xB681, 0x7640,
        0x7200, 0xB2C1, 0xB381, 0x7340, 0xB101, 0x71C0, 0x7080, 0xB041,
        0x5000, 0x90C1, 0x9181, 0x5140, 0x9301, 0x53C0, 0x5280, 0x9241,
        0x9601, 0x56C0, 0x5780, 0x9741, 0x5500, 0x95C1, 0x9481, 0x5440,
        0x9C01, 0x5CC0, 0x5D80, 0x9D41, 0x5F00, 0x9FC1, 0x9E81, 0x5E40,
        0x5A00, 0x9AC1, 0x9B81, 0x5B40, 0x9901, 0x59C0, 0x5880, 0x9841,
        0x8801, 0x48C0, 0x4980, 0x8941, 0x4B00, 0x8BC1, 0x8A81, 0x4A40,
        0x4E00, 0x8EC1, 0x8F81, 0x4F40, 0x8D01, 0x4DC0, 0x4C80, 0x8C41,
        0x4400, 0x84C1, 0x8581, 0x4540, 0x8701, 0x47C0, 0x4680, 0x8641,
        0x8201, 0x42C0, 0x4380, 0x8341, 0x4100, 0x81C1, 0x8081, 0x4040};
    return ((crc & 0xFF00) >> 8) ^ tbl[(crc & 0x00FF) ^ (data & 0x00FF)];
}

short calcula_CRC(unsigned char *commands, int size) {
	int i;
	short crc = 0;
	for(i=0;i<size;i++) {
		crc = CRC16(crc, commands[i]);
	}
	return crc;
}

int main(int argc, char ** argv) {
    //-------------------------
    //----- CONFIGURAÇÃO DA UART -----
    //-------------------------
    // At bootup, pins 8 and 10 are already set to UART0_TXD, UART0_RXD (ie the
    int uart0_filestream = -1;
    // ABRIR A UART
    // CONFIGURAÇÕES DEFINIDAS EM fcntl.h:
    // Modos de Acesso (utilize apensa 1 deles):
    // O_RDONLY - Abrir apenas para leitura.
    // O_RDWR - Abrir para Leitura / Escrita
    // O_WRONLY - Abrir apenas para Escrita.
    //
    // O_NDELAY / O_NONBLOCK (mesma função) - Habilita o modo não-blocante.
    // Quando configurado as solicitações de Leitura no arquivo podem retornar
    // imediatamente com erro quando não houverem dados disponíveis (Ao invés de
    // bloquear). Do mesmo modo, solicitações de escrita podem retornar erro
    // caso não seja possível escrever na saída.
    //
    // O_NOCTTY - Quando definido e o caminho identificar um dispositivo de
    // terminal, a função open() não causará que este terminal obtenha controle
    // do processo terminal.

    uart0_filestream = open("/dev/serial0", O_RDWR | O_NOCTTY | O_NDELAY); //Abrir no modo não blocante para Leitura / Escrita
    if (uart0_filestream == -1)
    {
        printf("Erro - Porta Serial nao pode ser aberta. Confirme se não está sendo usada por outra aplicação.\n");
    }
    struct termios options;
    tcgetattr(uart0_filestream, &options);
    options.c_cflag = B115200 | CS8 | CLOCAL | CREAD; // Set baud rate
    options.c_iflag = IGNPAR;
    options.c_oflag = 0;
    options.c_lflag = 0;
    tcflush(uart0_filestream, TCIFLUSH);
    tcsetattr(uart0_filestream, TCSANOW, &options);
    //-------------------------------------
    //----- TX - Transmissão de Bytes -----
    //-------------------------------------
    unsigned char tx_buffer[20];
    unsigned char *p_tx_buffer;
    p_tx_buffer = &tx_buffer[0];
    short crc;
    int conta_size = 0;
    unsigned char subcodigo = 0xC1;

    tx_buffer[conta_size++] = 0x01;
    tx_buffer[conta_size++] = (subcodigo > 0xD0) ? 0x23 : 0x16;
    tx_buffer[conta_size++] = subcodigo;
    tx_buffer[conta_size++] = 1;
    tx_buffer[conta_size++] = 8;
    tx_buffer[conta_size++] = 3;
    tx_buffer[conta_size++] = 6;

    crc = calcula_CRC(tx_buffer,conta_size);
    memcpy(tx_buffer + conta_size, (void*) &crc, sizeof(crc));
    
    conta_size+=sizeof(crc);

    if (uart0_filestream != -1)
    {
        int count = write(uart0_filestream, &tx_buffer[0], conta_size); 
        // Arquivo, bytes a serem escritos, número de bytes a
        if (count < 0)
        {
            printf("Erro na transmissao - UART TX\n");
        }
    }
    //-------------------------------------
    //----- RX - Leitura de Bytes -----
    //-------------------------------------
    if (uart0_filestream != -1)
    {
        // Ler até 255 caracteres da porta de entrada
        unsigned char rx_buffer[256];
        int rx_length = read(uart0_filestream, (void*)rx_buffer,255); //Arquivo, buffer de saída, número máximo de caracteres a serem lidos
        if (rx_length < 0)
        {
            perror("Falha na leitura\n");
            return -1;
        }
        else if (rx_length == 0)
        {
            printf("Nenhum dado disponivel\n");
        }
        else
        {
            //Bytes received
            rx_buffer[rx_length] = '\0';
            printf("%i bytes lidos : %s\n", rx_length, rx_buffer);
        }
    }
    //----- CLOSE THE UART -----
    close(uart0_filestream);
    return 0;
}