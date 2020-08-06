/* ===========================================
 * Algoritmo que laz a leitura do LM35
 * e converte em kelvin(K) e fahrenheit(°F)
 * e tambem um teste de leds
 * 
 * Integration with Python Interface (tkinter)
 * ===========================================
 */

const int sensor = A0;                         // Pino AN0 para leitura do sensor
int value_sensor = 0;                          // variable to store the value sensor

int led = 8;                                   // Pino onde o led está D8
char serial_rd;                                // Variavel que recebe o que foi enviado pela interface

void setup(){
  Serial.begin(9600);                          // iniciando comunicação
  pinMode(led, OUTPUT);                        // Define o led como saída
  pinMode(sensor, INPUT);                      // Define sensor como entrada
}

void loop()
{
  if(Serial.available())
  {

    serial_rd = Serial.read();                // Recebe o que foi enviado pela interface 
    
    if(serial_rd == '1'){
      digitalWrite(led, HIGH);                // If(Se) receber 1 liga o led
    }
    if(serial_rd == '2'){
      digitalWrite(led, LOW);                 // If(Se) receber 2 desliga o led  
    }
    
    value_sensor = analogRead(sensor);        // Variavel que armazena o valor do sensor 0 - 1023

    // Convertendo os valores de (bits) para ser como medidas de temperaturas
    
    value_sensor = value_sensor * 500;       // o sensor está ligado a 5 volts e ele envia 0.01 volt por grau
    value_sensor = value_sensor / 1023;      // e dividindo por 1023 conseguimos o valor real de leitura em °C
 
    Serial.println(value_sensor);            // Escreve/envia o valor pela serial  
    delay(1000);
  }
}
