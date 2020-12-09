#include <arduino.h>
#define IN 8
#define OUT 9

#define LED_vermelho 2
#define LED_verde 3

int VET_INFO [5];
String INFO = "";
bool flag = LOW;

byte var_info = 0;

long temp;

void setup() 
{
 Serial.begin(9600);
  pinMode(IN, INPUT);
  pinMode(OUT, OUTPUT);
  pinMode(LED_vermelho, OUTPUT);
  pinMode(LED_verde, OUTPUT);
  digitalWrite(LED_vermelho, HIGH);
}

void loop() 
{
  pisca();
}

void pisca()
{
  switch(var_info)
  {
    case 0: temp = millis(); break;
    case 1: 
      if (millis() - temp> 250)
      {
        temp = millis();
        digitalWrite(LED_verde, !digitalRead(LED_verde));
        digitalWrite(LED_vermelho, !digitalRead(LED_vermelho));
      }
    break;
    case 2: 
      if (millis() - temp> 250)
      {
        temp = millis();
        digitalWrite(LED_verde, LOW);
        digitalWrite(LED_vermelho, !digitalRead(LED_vermelho));
      }
    break;
    case 3: 
      if (millis() - temp> 250)
        {
          temp = millis();
          digitalWrite(LED_verde, !digitalRead(LED_verde));
          digitalWrite(LED_vermelho, LOW);
        }
    break;
  }
}

void informacao()
{
  digitalWrite(LED_verde, LOW);
  digitalWrite(LED_vermelho, HIGH);
  var_info = 0;
  digitalWrite(OUT, HIGH);
  delay(100);
  for(byte i = 1; i <= 5; i++)
  {
    digitalWrite(OUT, (int(INFO[i])-48));
    delay(200);
  }
  digitalWrite(OUT, LOW);
  while(digitalRead(IN) == LOW);
  Serial.print("O");

  delay(1000);
  digitalWrite(LED_verde, HIGH);
  digitalWrite(LED_vermelho, LOW);
}

void serialEvent() 
{
char letra = Serial.read();
  switch(letra)
  {
    case 'a': INFO = String(32+1, BIN); informacao(); break; //Setor 0 da malha
    case 'c': INFO = String(32+2, BIN); informacao(); break; //Setor 1 da malha
    case 'd': INFO = String(32+3, BIN); informacao(); break; //Setor 2 da malha
    case 'e': INFO = String(32+4, BIN); informacao(); break; //Setor 3 da malha
    case 'f': INFO = String(32+5, BIN); informacao(); break; //Setor 4 da malha
    case 'g': INFO = String(32+6, BIN); informacao(); break; //Setor 5 da malha
    case 'h': INFO = String(32+7, BIN); informacao(); break; //Setor 6 da malha
    case 'i': INFO = String(32+8, BIN); informacao(); break; //Setor 7 da malha
    case 'j': INFO = String(32+9, BIN); informacao(); break; //Setor 8 da malha

    case 'k': var_info = 1; Serial.print("O");break; //Deu velha, as duas luzes irão piscar de forma alternada
    case 'l': var_info = 2; Serial.print("O");break; //Vitória do robô, a luz vermelha irá piscar
    case 'm': var_info = 3; Serial.print("O");break; //Vitória da pessoa, a luz verde irá piscar 
    
    
    

    case 'w': INFO = String(32+10, BIN); informacao(); break; //Pedir para o robô fazer a malha

  }
  
}
