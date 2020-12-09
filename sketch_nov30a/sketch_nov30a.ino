String nome,idade,Tchifre,frase;
v
void setup() 
{
  Serial.begin(9600);
  Serial.println("Olá, qual seu nome?");
  
  nome = Input();
  frase = "Olá " + nome + " quantos anos voce tem? \n";
  Serial.print(frase);
  frase = "";
  
  idade = Input();
  frase = "Legal " + nome + " você tem " + idade + " anos! Qual é o tamanho do seu chifre? Em cm claro.\n";
  Serial.print(frase);
  frase = "";

  Tchifre = Input();
  frase = "WOOOOOOOOW CORNAO VOCE HEIN, COM " + Tchifre + " CM DE CHIFRE, FICA DIFICIL ATÉ PASSAR PELA PORTA HEIN!!";
  Serial.print(frase);
  frase = "";
}

void loop() 
{
  
}




String Input()
{
  String Temp = "";
  
  while (Serial.available() == 0); //Aguarda a pessoa escrever algo
  
    while (Serial.available() > 0) //Enquanto tiver informação disponível, ele vai concatenar na string
  {
    char letra = Serial.read();
    if (letra != '\n') Temp += letra;
    delay(10);
  }

  return Temp; 
}
