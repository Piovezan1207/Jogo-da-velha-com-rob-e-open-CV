#define IN 8
#define OUT 9

int VET_INFO [5];
bool flag = LOW;
void setup() 
{
 Serial.begin(9600);
  pinMode(IN, INPUT);
  pinMode(OUT, OUTPUT);
}

void loop() 
{
  if(flag == HIGH)
  {
    delay(100);
  
  }
  
}

void informacao()
{
  digitalWrite(OUT, HIGH);
  delay(250);

for(byte i = 0; i <5; i++)
{
  digitalWrite(OUT, VET_INFO[i]);
  delay(500);
}
digitalWrite(OUT, LOW);
while(digitalRead(IN) == LOW);
Serial.print("O");
flag = HIGH;
}

void serialEvent() 
{
char letra = Serial.read();
  switch(letra)
  {
    case 'a':  //Setor 0 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 0;
    VET_INFO[2] = 0;
    VET_INFO[3] = 0;
    VET_INFO[4] = 1;
    informacao();
    break;

    case 'c':  //Setor 1 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 0;
    VET_INFO[2] = 0;
    VET_INFO[3] = 1;
    VET_INFO[4] = 0; 
    informacao();
    break;

    case 'd':  //Setor 2 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 0;
    VET_INFO[2] = 0;
    VET_INFO[3] = 1;
    VET_INFO[4] = 1; 
    informacao();
    break;

    case 'e':  //Setor 3 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 0;
    VET_INFO[2] = 1;
    VET_INFO[3] = 0;
    VET_INFO[4] = 0; 
    informacao();
    break;

    case 'f':  //Setor 4 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 0;
    VET_INFO[2] = 1;
    VET_INFO[3] = 0;
    VET_INFO[4] = 1; 
    informacao();
    break;

    case 'g':  //Setor 5 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 0;
    VET_INFO[2] = 1;
    VET_INFO[3] = 1;
    VET_INFO[4] = 0; 
    informacao();
    break;

    case 'h':  //Setor 6 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 0;
    VET_INFO[2] = 1;
    VET_INFO[3] = 1;
    VET_INFO[4] = 1; 
    informacao();
    break;

    case 'i':  //Setor 7 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 1;
    VET_INFO[2] = 0;
    VET_INFO[3] = 0;
    VET_INFO[4] = 0; 
    informacao();
    break;

    case 'j':  //Setor 8 da malha
    VET_INFO[0] = 0; 
    VET_INFO[1] = 1;
    VET_INFO[2] = 0;
    VET_INFO[3] = 0;
    VET_INFO[4] = 1; 
    informacao();
    break;

    case 'W':
    digitalWrite(OUT, HIGH);
    delay(400);
    digitalWrite(OUT, LOW);
    delay(400);

    while(digitalRead(IN) == LOW);

    flag = HIGH;
    Serial.print("O");
    break;

    case 'V': flag = LOW; break;
  }
  
  //Serial.println(letra);
 
   //delay(2000);

}
