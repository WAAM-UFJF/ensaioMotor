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
  float corrente[50];
  float tempo[50];
  // Direção == False -> Anti-horario    ;    Direção == True  ->  Horário
  float shuntvoltage = 0;  
  float busvoltage = 0;    
  float current_mA = 0;    
  float loadvoltage = 0;   
  float power_mW = 0;

  shuntvoltage = ina219_0.getShuntVoltage_mV();    
  busvoltage = ina219_0.getBusVoltage_V();         
  current_mA = ina219_0.getCurrent_mA();           
  power_mW = ina219_0.getPower_mW();               
  loadvoltage = busvoltage + (shuntvoltage / 1000);  
  

  for(int i=0; i<50 ; i++){
    corrente[i] = ina219_0.getCurrent_mA();
    tempo[i] = millis();
  }

  Serial.println(corrente[20]);
}