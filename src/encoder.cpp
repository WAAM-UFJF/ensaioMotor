#include <Arduino.h>


// Definições do Encoder
const int Encoder_C1 = 12;
const int Encoder_C2 = 14;
byte Encoder_C1Last;
int duracao;
boolean Direcao;


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
  //Serial.println("Iniciei o Encoder");
  pinMode(Encoder_C2, INPUT);
  attachInterrupt(14, calculapulso, CHANGE);
}
