#include <Arduino.h>

int resolucaoEncoder = 400;
int phi = PI;
float w;
extern int deltaT;

void measureVelocity(){
    w = 1000.0*phi/deltaT;
    Serial.print(w);
    Serial.print(";");
    // w = phi/(deltaT/1000);
    // Serial.print(w);
    // Serial.print(";");
}