#include <stdio.h>
#include <unistd.h> //Usado para a UART
#include <fcntl.h> //Usado para a UART
#include <termios.h> //Usado para a UART
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

    *p_tx_buffer++ = 0x01;
    *p_tx_buffer++ = 'e';
    *p_tx_buffer++ = 's';
    *p_tx_buffer++ = 't';
    *p_tx_buffer++ = 'e';

    printf("10");
    printf("%s",p_tx_buffer);

    return 0;

    if (uart0_filestream != -1)
    {
        int count = write(uart0_filestream, &tx_buffer[0], (p_tx_buffer - &tx_buffer[0])); 
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