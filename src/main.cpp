#include <Arduino.h>
#include <encoder.h>
#include <Wire.h> 
#include <Adafruit_INA219.h>
#include <time.h>
#include <ArduinoJson.h>

#define SDA 21
#define SCL 22

// Definições do PWM e Ponte H
const int led  = 16;          // Define a porta de saída do sinal PWM.
const int sentidoMotor1 = 2;  // Porta para definir o sentido de rotação 1.
const int sentidoMotor2 = 0;  // Porta para definir o sentido de rotação 2.

const int freq = 5000;        // Define a frequencia a ser utilizada
const int ledChannel = 0;
int resolution = 8;           // Define a resolução que será utilizada no PWM.


// Definição do sensor de corrente e tensão.
Adafruit_INA219 ina219_0 (0x40);

// Definições JSON
DynamicJsonDocument doc(32);

// Define o valor de amostras para a media movel
int N = 128;
float n = 1.0/N;
float mediaMovel[128];
int contador=0;

void setup() {
  Serial.begin(115200);
  pinMode(sentidoMotor1, OUTPUT);
  pinMode(sentidoMotor2, OUTPUT);
  pinMode(led, OUTPUT);
  

  // Atribui o canal ao GPIO que será controlado
  ledcAttachPin(led, ledChannel);

  // Configura o LED PWM
  ledcSetup(ledChannel, freq, resolution);  
  ledcWrite(ledChannel, 255);

  // Define como output os pinos que definem o sentido de rotação do motor
  digitalWrite(sentidoMotor1, LOW);
  digitalWrite(sentidoMotor2, HIGH);

  // Inicializa o sensor INA219
  if (! ina219_0.begin()) {
    Serial.println("Falha ao encontrar o INA219");
    while (1) { delay(10); }
  } 
  ina219_0.setCalibration_16V_400mA();
  // Inicializa o encoder
  EncoderInit();
}



void loop() {
  float corrente = 0, tempo = 0, correnteFiltrada = 0;
  contador++;
  for(int i = 0; i < 5; i++){
    corrente = corrente + ina219_0.getCurrent_mA();
    tempo = tempo + millis();
  }

  tempo = tempo/5;
  corrente = corrente/5;
  mediaMovel[(contador-1)%N] = corrente;

  if(contador < N){
    for(int i=0; i<contador+1;i++){
      correnteFiltrada += mediaMovel[i];
    }
    correnteFiltrada = correnteFiltrada/contador;
  }
  else{
    for(int i=0; i<N; i++){
      correnteFiltrada += mediaMovel[i];
    }
    correnteFiltrada = correnteFiltrada*n;    
  }
  Serial.print(tempo);
  Serial.print(";");
  Serial.println(correnteFiltrada);
  delay(3);
}