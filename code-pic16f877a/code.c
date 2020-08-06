#define red RB0_bit                 // Pin as output to led-red

char uart_rd;
char txt[7];                        // Auxiliary variable
long int valueAD = 0;               // Values LM35

void main() {
  CMCON = 0x07;                     // Comparators desable

  ADCON0 = 0x01;                    // Configure writing analogic
  ADCON1 = 0x0E;                    // AN0

  TRISB = 0x80;                     // Set RB7 as output
  PORTB = 0x00;                     // Set all ports initializing a low power

  UART1_Init(9600);               // Initialize UART module at 9600 bps
  Delay_ms(100);                  // Wait for UART module to stabilize

  while (1) {                     // Endless loop
    if (UART1_Data_Ready()) {     // If data is received,
      uart_rd = UART1_Read();     // read the received data,
                                  // and send data via UART
    }

    valueAD = ADC_Read(0);         // Read channel AN0

    valueAD = valueAD * 500;       // Value adjust for sensor LM35

    valueAD = valueAD/1023;        // Referent a conversion AD 10 bits

    IntToStr(valueAD, txt);        // Convert valorAD in string

    UART1_Write_Text(txt);         // Write in virtual serial in proteus
    UART1_Write(13);
    UART1_Write(10);
    delay_ms(1000);

    if (uart_rd == '1'){
       red = 0x01;
    }
    if(uart_rd == '2'){
       red = 0x00;
    }

  }
}