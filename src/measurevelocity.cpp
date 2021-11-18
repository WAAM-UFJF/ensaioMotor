#include <Arduino.h>
#include<measurecurrent.h>

int resolucaoEncoder = 400;
double phi = 0.25*PI;
float w;
extern int deltaT;

static const int N = 128;
static const float n = 1.0/N;
static float mediaMovel[N];
static int contador = 0;

void measureVelocity(){
    float w = 0, wFiltrada = 0;
    contador++;
    w = 1000.0*phi/deltaT;

    mediaMovel[(contador-1)%N] = w;

    if(contador < N){
        for(int i=0; i<contador+1;i++){
            wFiltrada += mediaMovel[i];
        }
        wFiltrada = wFiltrada/contador;
    }
    else{
        for(int i=0; i<N; i++){
            wFiltrada += mediaMovel[i];
        }
        wFiltrada = wFiltrada*n;    
    }
    Serial.print(wFiltrada);
    Serial.print(";");
}