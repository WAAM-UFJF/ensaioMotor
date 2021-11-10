#include <Arduino.h>

// Pino para alterar PWM
const int pinAlteraPWM = 15;

// Configurações PWM
const int motor  = 16;          // Define a porta de saída do sinal PWM.
const int freq = 5000;        // Define a frequencia a ser utilizada
const int motorChannel = 0;
int resolution = 8;           // Define a resolução que será utilizada no PWM.

int degrau = 0;

void alteraPWM(){
    ledcWrite(motorChannel, 180);
    degrau =1;
}

void verificaPWM()
{
    pinMode(pinAlteraPWM, INPUT);
    attachInterrupt(pinAlteraPWM, alteraPWM, RISING);
}

void inicializaPWM()
{
    pinMode(motor, OUTPUT);

    // Atribui o canal ao GPIO que será controlado
    ledcAttachPin(motor, motorChannel);

    // Configura o LED PWM
    ledcSetup(motorChannel, freq, resolution);  
    ledcWrite(motorChannel, 154);

}