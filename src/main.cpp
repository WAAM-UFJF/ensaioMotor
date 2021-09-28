#include <Arduino.h>
#include <Wire.h> 
#include <Adafruit_INA219.h>

#define SDA 21
#define SCL 22

// Definições do PWM e Ponte H
const int led  = 16;          // Define a porta de saída do sinal PWM.
const int sentidoMotor1 = 2;  // Porta para definir o sentido de rotação 1.
const int sentidoMotor2 = 0;  // Porta para definir o sentido de rotação 2.

const int freq = 5000;        // Define a frequencia a ser utilizada
const int ledChannel = 0;
int resolution = 8;           // Define a resolução que será utilizada no PWM.

// Definições do Encoder
const int Encoder_C1 = 12;
const int Encoder_C2 = 14;
byte Encoder_C1Last;
int duracao;
boolean Direcao;

// Definição do sensor de corrente e tensão.
Adafruit_INA219 ina219_0 (0x40);

void calculapulso()
{
  int Lstate = digitalRead(Encoder_C1);
  if ((Encoder_C1Last == LOW) && Lstate == HIGH)
  {
    int val = digitalRead(Encoder_C2);
    if (val == LOW && Direcao)
    {
      Direcao = false; //Reverse
    }
    else if (val == HIGH && !Direcao)
    {
      Direcao = true;  //Forward
    }
  }
  Encoder_C1Last = Lstate;
  if (!Direcao)  duracao++;
  else  duracao--;
}

void EncoderInit()
{
  Serial.println("Iniciei o Encoder");
  pinMode(Encoder_C2, INPUT);
  attachInterrupt(14, calculapulso, CHANGE);
}


void setup() {
  Serial.begin(115200);
  pinMode(sentidoMotor1, OUTPUT);
  pinMode(sentidoMotor2, OUTPUT);
  pinMode(led, OUTPUT);
  

  // Atribui o canal ao GPIO que será controlado
  ledcAttachPin(led, ledChannel);

  // Configura o LED PWM
  ledcSetup(ledChannel, freq, resolution);  

  // Define como output os pinos que definem o sentido de rotação do motor
  digitalWrite(sentidoMotor1, LOW);
  digitalWrite(sentidoMotor2, HIGH);

  // Inicializa o sensor INA219
  if (! ina219_0.begin()) {
    Serial.println("Falha ao encontrar o INA219");
    while (1) { delay(10); }
  } 

  // Inicializa o encoder
  EncoderInit();
}

void loop() {
  float shuntvoltage = 0;  
  float busvoltage = 0;    
  float current_mA = 0;    
  float loadvoltage = 0;   
  float power_mW = 0;

  ledcWrite(ledChannel, 255);
  Serial.print("DutyCycle: 255 \n");

  shuntvoltage = ina219_0.getShuntVoltage_mV();    
  busvoltage = ina219_0.getBusVoltage_V();         
  current_mA = ina219_0.getCurrent_mA();           
  power_mW = ina219_0.getPower_mW();               
  loadvoltage = busvoltage + (shuntvoltage / 1000);  

  Serial.print("Tensão de Entrada:   "); Serial.print(busvoltage); Serial.println(" V"); 
  Serial.print("Tensão no shunt: "); Serial.print(shuntvoltage); Serial.println(" mV");  
  Serial.print("Tensão da Carga:  "); Serial.print(loadvoltage); Serial.println(" V");   
  Serial.print("Corrente:       "); Serial.print(current_mA); Serial.println(" mA");     
  Serial.print("Potência:         "); Serial.print(power_mW); Serial.println(" mW");     
  
  if(Direcao == false){
    Serial.println("Sentido: Anti-horário");
  }
  else{
    Serial.println("Sentido: Horário");
  }
  Serial.println("");

  delay(5000);

  //  // Aumenta a velocidade de rotação do motor
  // for(int dutyCycle = 200; dutyCycle <= (pow(2, resolution) - 1); dutyCycle++){   
  //   // Aumenta a velocidade de rotação do motor através do aumento do dutycycle do PWM
  //   ledcWrite(ledChannel, dutyCycle);
  //   Serial.print("DutyCycle: ");
  //   Serial.println(dutyCycle);

  //   shuntvoltage = ina219_0.getShuntVoltage_mV();    
  //   busvoltage = ina219_0.getBusVoltage_V();         
  //   current_mA = ina219_0.getCurrent_mA();           
  //   power_mW = ina219_0.getPower_mW();               
  //   loadvoltage = busvoltage + (shuntvoltage / 1000);

  //   Serial.print("Tensão de Entrada:   "); Serial.print(busvoltage); Serial.println(" V"); 
  //   Serial.print("Tensão no shunt: "); Serial.print(shuntvoltage); Serial.println(" mV");  
  //   Serial.print("Tensão da Carga:  "); Serial.print(loadvoltage); Serial.println(" V");   
  //   Serial.print("Corrente:       "); Serial.print(current_mA); Serial.println(" mA");     
  //   Serial.print("Potência:         "); Serial.print(power_mW); Serial.println(" mW");     
  //   Serial.println("");
  //   delay(5000);
  // }

  // // Diminui a valocidade de rotação do motor
  // for(int dutyCycle = (pow(2, resolution) - 1); dutyCycle >= 0; dutyCycle--){
  //   // Diminui a velocidade de rotação do motor através do decremento do dutycycle do PWM
  //   ledcWrite(ledChannel, dutyCycle);
  //   Serial.print("DutyCycle: ");
  //   Serial.println(dutyCycle);

  //   shuntvoltage = ina219_0.getShuntVoltage_mV();    
  //   busvoltage = ina219_0.getBusVoltage_V();         
  //   current_mA = ina219_0.getCurrent_mA();           
  //   power_mW = ina219_0.getPower_mW();               
  //   loadvoltage = busvoltage + (shuntvoltage / 1000);
    
  //   Serial.print("Tensão de Entrada:   "); Serial.print(busvoltage); Serial.println(" V"); 
  //   Serial.print("Tensão no shunt: "); Serial.print(shuntvoltage); Serial.println(" mV");  
  //   Serial.print("Tensão da Carga:  "); Serial.print(loadvoltage); Serial.println(" V");   
  //   Serial.print("Corrente:       "); Serial.print(current_mA); Serial.println(" mA");     
  //   Serial.print("Potência:         "); Serial.print(power_mW); Serial.println(" mW");     
  //   Serial.println("");
  //   delay(500);
  // }

}

