void informacao(String INFO )
{
  digitalWrite(LED_verde, LOW);
  digitalWrite(LED_vermelho, HIGH);
  
  digitalWrite(OUT, HIGH);
  delay(250);
  for(byte i = 1; i <= 5; i++)
  {
    digitalWrite(OUT, (int(INFO[i])-48));
    delay(500);
  }
  digitalWrite(OUT, LOW);
  flag_info = HIGH;
}
