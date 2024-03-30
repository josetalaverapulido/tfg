
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "model.h"

WiFiClient esp32Client;
PubSubClient mqttClient(esp32Client);

char ssid[] = "vodafoneC080";
char password[] = "JoSE.carCHEleJO.arBOL";
char MQTT_CLIENT_NAME[] = "2";
char server[] = "2";
int port = 2;
char receive_topic[] = "22";
char send_topic[] = "2";



String receivedMessage = "";

const int MAX_JSON_SIZE = 512; // Tamaño máximo del JSON
const int MAX_VALUES = 20;     // Número máximo de valores que podemos almacenar

// Definir el tamaño de la matriz para almacenar múltiples valores de temperatura y humedad
const int NUM_READINGS = 24;
float readings[NUM_READINGS][2]; // [indice][0] para temperatura, [indice][1] para humedad


void printReadings() {
  for (int i = 0; i < NUM_READINGS; i++) {
    Serial.print("Temperatura ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(readings[i][0]);
    Serial.print("Humedad ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(readings[i][1]);
  }
}



void wifiInit() {
  Serial.print("Conectándose a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
  }
  Serial.println("");
  Serial.println("Conectado a WiFi");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}


void sendText(const char* text) {
  mqttClient.publish(send_topic, text);
}

void OnMqttReceived(char *topic, byte *payload, unsigned int length)
{
    Serial.print("Received on ");
    Serial.print(topic);
    Serial.print(": ");

    // Extract the received text
    String receivedText = "";
    for (int i = 0; i < length; i++) {
        receivedText += (char)payload[i];
    }

    Serial.println(receivedText); // Print received text to serial monitor
    
    // Send the received text to the "send" topic
    sendText(receivedText.c_str());
}



void ConnectMqtt()
{
    Serial.print("Starting MQTT connection...");
    if (mqttClient.connect(MQTT_CLIENT_NAME))
    {
        mqttClient.subscribe(receive_topic);
        Serial.println("Connected");
        //mqttClient.publish("connected","Entrada/01");
    }
    else
    {
        Serial.print("Failed MQTT connection, rc=");
        Serial.print(mqttClient.state());
        Serial.println(" try again in 5 seconds");

        delay(5000);
    }
}

void setup() {
  Serial.begin(115200);
  delay(10);
  wifiInit();
  mqttClient.setServer(server, port);
  mqttClient.setBufferSize(1024); // SÚPER IMPORTANTE!!!!!!!!!!!!!!!!!!!!
  mqttClient.setCallback(OnMqttReceived);

  // Inicializar los valores a 0
  for (int i = 1; i < NUM_READINGS; i++) {
  readings[i][0] = 0;
  readings[i][1] = 0;
  }
}

void loop() {
  if (!mqttClient.connected()) {
    ConnectMqtt();
  }
  mqttClient.loop();
}

    