#include <Arduino.h>
#include <encoder.h>
#include <confpwm.h>
#include <Wire.h> 
#include <Adafruit_INA219.h>
#include <time.h>
#include <ArduinoJson.h>

#define SDA 21
#define SCL 22

// Definições do PWM e Ponte H

const int sentidoMotor1 = 2;  // Porta para definir o sentido de rotação 1.
const int sentidoMotor2 = 0;  // Porta para definir o sentido de rotação 2.




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

  // Define como output os pinos que definem o sentido de rotação do motor
  digitalWrite(sentidoMotor1, LOW);
  digitalWrite(sentidoMotor2, HIGH);

  // Inicializa o sensor INA219
  while (1){
    if(ina219_0.begin()){
      break;
    }
    Serial.println("Falha ao encontrar o INA219");
    delay(20);
  }
  ina219_0.setCalibration_16V_400mA();

  // Inicializa o PWM do motor com D = 0.6
  inicializaPWM();

  // Inicializa o encoder
  EncoderInit();

  // Altera PWM
  verificaPWM();
}



void loop() {
  float corrente = 0, tempo = 0, correnteFiltrada = 0;
  contador++;

  tempo = millis();
  corrente = ina219_0.getCurrent_mA();

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
  delay(9);
}