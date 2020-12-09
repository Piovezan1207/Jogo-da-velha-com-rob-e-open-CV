#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <ESP8266WebServer.h>
//#include <ESP8266mDNS.h>

#define IN 14 //D5
#define OUT 12 //D6

#define LED_vermelho 13 //D7
#define LED_verde 15 //D8

#ifndef STASSID
#define STASSID "Planta 4.0"
#define STAPSK  "Planta40@eniacehdiferente"
#endif

bool flag_info = LOW;


const char* ssid     = STASSID;
const char* password = STAPSK;

ESP8266WebServer server(9090);




void handleRoot() {
  Serial.println(server.arg("plain"));
  //server.send(200, "text/html", postForms);
}

void Post_robo() // https://ip:porta/postplain/ - Função que é execultada quando chega a requisição
{ 
  if (server.method() != HTTP_POST) {
    server.send(405, "text/plain", "Method Not Allowed");
  } 
  else 
  {
    String Req = server.arg("plain");
    Serial.println(Req);

    int num = Req.toInt();
    String INFO = String(32+num, BIN); //informacao();
    Serial.println(INFO);
    server.send(200, "text/plain", "Ok"); 
    informacao(INFO); 
  }
}


void handleNotFound() {
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
}

void setup(void) {
  pinMode(IN, INPUT);
  pinMode(OUT, OUTPUT);
  pinMode(LED_vermelho, OUTPUT);
  pinMode(LED_verde, OUTPUT);
  digitalWrite(LED_vermelho, HIGH);
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

 /* if (MDNS.begin("esp8266")) {
    Serial.println("MDNS responder started");
  }*/

  server.on("/", handleRoot);

  server.on("/robo/", Post_robo);

  server.onNotFound(handleNotFound);

  server.begin();
  Serial.println("HTTP server started");
}

void loop(void) {
  server.handleClient();
  if(flag_info and digitalRead(IN))
  {
    flag_info = LOW;
    Serial.print("O");
    delay(2000);
    digitalWrite(LED_verde, HIGH);
    digitalWrite(LED_vermelho, LOW);
  }
}
