#include <Arduino.h>

int resolucaoEncoder = 400;
int phi = PI;
float w;
extern int deltaT;

void measureVelocity(){
    w = 1000.0*phi/(2*deltaT);
    Serial.print(w);
    Serial.print(";");
}