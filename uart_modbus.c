#include <stdio.h>
#include <unistd.h> //Usado para a UART
#include <fcntl.h> //Usado para a UART
#include <termios.h> //Usado para a UART
#include <string.h>

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
    // uart0_filestream = open("/dev/serial0", O_RDWR | O_NOCTTY |
    // O_NDELAY); //Abrir no modo não blocante para Leitura / Escrita
    // if (uart0_filestream == -1)
    // {
    //     printf("Erro - Porta Serial nao pode ser aberta. Confirme se não está sendo usada por outra aplicação.\n");
    // }
    //CONFIGURAÇÕES DA UART
    // Flags (Definidas em /usr/include/termios.h):
    // Baud rate:- B1200, B2400, B4800, B9600, B19200, B38400, B57600, B115200,
    // B230400, B460800, B500000, B576000, B921600, B1000000, B1152000, B1500000,
    // B2000000, B2500000, B3000000, B3500000, B4000000
    // CSIZE:- CS5, CS6, CS7, CS8
    // CLOCAL - Ignore modem status lines
    // CREAD - Enable receiver
    // IGNPAR = Ignore characters with parity errors
    // ICRNL - Map CR to NL on input
    // PARENB - Parity enable
    // PARODD - Odd parity

short CRC16(short crc, unsigned char data)
{
    const short tbl[256] = {
        0x0000, 0xC0C1, 0xC181, 0x0140, 0xC301, 0x03C0, 0x0280, 0xC241,
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

int conta_size = 0;

unsigned char *monta_mensagem(unsigned char *tx_buffer, unsigned char subcodigo){

    conta_size = 0;
    short crc;

    tx_buffer[conta_size++] = 0x01;
    tx_buffer[conta_size++] = (subcodigo > 0xD0) ? 0x23 : 0x16;
    tx_buffer[conta_size++] = subcodigo;
    tx_buffer[conta_size++] = 1;
    tx_buffer[conta_size++] = 8;
    tx_buffer[conta_size++] = 3;
    tx_buffer[conta_size++] = 6;

    printf("\n");
    crc = calcula_CRC(tx_buffer,conta_size);

    memcpy(tx_buffer + conta_size, (void*) &crc, sizeof(crc));
    
    conta_size+=sizeof(crc);

    for(int i = 0; i < conta_size;i++)
    {
        printf("%d : %ld\n",tx_buffer[i],sizeof(tx_buffer[i]));
    }

    return tx_buffer;
}

int main(int argc, char ** argv) {
    //-------------------------
    //----- CONFIGURAÇÃO DA UART -----
    //-------------------------
    // At bootup, pins 8 and 10 are already set to UART0_TXD, UART0_RXD (ie the
    int uart0_filestream = -1;

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
    conta_size = 0;
    short crc;

    unsigned char subcodigo = 0xC1;

    tx_buffer[conta_size++] = 0x01;
    tx_buffer[conta_size++] = (subcodigo > 0xD0) ? 0x23 : 0x16;
    tx_buffer[conta_size++] = subcodigo;
    tx_buffer[conta_size++] = 1;
    tx_buffer[conta_size++] = 8;
    tx_buffer[conta_size++] = 3;
    tx_buffer[conta_size++] = 6;

    printf("\n");
    crc = calcula_CRC(tx_buffer,conta_size);

    memcpy(tx_buffer + conta_size, (void*) &crc, sizeof(crc));
    
    conta_size+=sizeof(crc);

    if (uart0_filestream != -1)
    {
        int count = write(uart0_filestream, &tx_buffer, conta_size ); 
        // Arquivo, bytes a serem escritos, número de bytes a
        // serem escritos;
        if (count < 0)
        {
            printf("Erro na transmissao - UART TX\n");
        }
    }
    //  -------------------------------------
    //  ----- RX - Leitura de Bytes ---------
    //  -------------------------------------
    sleep(1);
    if (uart0_filestream != -1)
    {
        // Ler até 255 caracteres da porta de entrada
        unsigned char rx_buffer[256];
        int rx_length = read(uart0_filestream, (void*)rx_buffer,255); 
        //Arquivo, buffer de saída, número máximo de caracteres a serem lidos
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
    // ----- CLOSE THE UART -----
    close(uart0_filestream);
    return 0;
}