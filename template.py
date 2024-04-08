def generar_codigo_arduino(ssid, password, mqtt_client_name, server, port, receive_topic, send_topic):
    codigo_arduino = f'''
#include <WiFi.h> // For connecting ESP32 to WiFi
#include <PubSubClient.h>
#include "model.h"
#include <ArduinoJson.h>
#include <ArduinoOTA.h>  // For enabling over-the-air updates

WiFiClient esp32Client;
PubSubClient mqttClient(esp32Client);

char ssid[] = "{ssid}";
char password[] = "{password}";
char MQTT_CLIENT_NAME[] = "{mqtt_client_name}";
char server[] = "{server}";
int port = {port};
char receive_topic[] = "{receive_topic}";
char send_topic[] = "{send_topic}";



// Initiate WiFi connection
void wifiInit() {{
  Serial.print("Conectándose a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {{
    Serial.print(".");
    delay(500);
  }}
  Serial.println("");
  Serial.println("Conectado a WiFi");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}}


// callback to execute when a message is received
void OnMqttReceived(char* topic, byte* payload, unsigned int length) {{
  // Crear un buffer para almacenar el payload como una cadena
  char json[length + 1];
  memcpy(json, payload, length);
  json[length] = '\0';

  // Analizar el JSON recibido
  DynamicJsonDocument doc(1024);
  DeserializationError error = deserializeJson(doc, json);

  // Verificar si ocurrió un error durante el análisis del JSON
  if (error) {{
    Serial.print("Error al analizar el JSON: ");
    Serial.println(error.c_str());
    return;
  }}

  // Variable para indicar si todos los valores son correctos
  bool todosCorrectos = true;

  // Verificar si el JSON contiene solo un campo y es uno de los esperados
  if (doc.size() == 1) {{
    if (doc.containsKey("value")) {{
      JsonArray valueArray = doc["value"].as<JsonArray>();
      for (int i = 0; i < valueArray.size(); i++) {{
        if (!valueArray[i].is<float>()) {{
          todosCorrectos = false;
          break;
        }}
      }}
      if (todosCorrectos) {{
        for (int i = 0; i < valueArray.size(); i++) {{
          Serial.print("[");
          Serial.print(valueArray[i].as<float>(), 2); // Imprime solo 2 decimales
          Serial.println("]");

        }}
      }} else {{
        Serial.println("Error: El valor no es un número flotante.");
      }}
    }} else if (doc.containsKey("array")) {{
      JsonArray array = doc["array"].as<JsonArray>();
      for (int i = 0; i < array.size(); i++) {{
        if (!array[i].is<float>()) {{
          todosCorrectos = false;
          break;
        }}
      }}
      if (todosCorrectos) {{
          Serial.print("[");
          for (int i = 0; i < array.size(); i++) {{
              Serial.print(array[i].as<float>(), 2); // Imprime solo 2 decimales
              if (i < array.size() - 1) {{
                  Serial.print(", ");
              }}
          }}
          Serial.println("]");
      }} else {{
        Serial.println("Error: Uno o más valores no son números flotantes.");
      }}
    }} else if (doc.containsKey("bi-array")) {{
      JsonArray biArray = doc["bi-array"].as<JsonArray>();
      for (int i = 0; i < biArray.size(); i++) {{
        JsonArray innerArray = biArray[i].as<JsonArray>();
        for (int j = 0; j < innerArray.size(); j++) {{
          if (!innerArray[j].is<float>()) {{
            todosCorrectos = false;
            break;
          }}
        }}
        if (!todosCorrectos) {{
          break;
        }}
      }}
      if (todosCorrectos) {{
        Serial.print("[");
        for (int i = 0; i < biArray.size(); i++) {{
            JsonArray innerArray = biArray[i].as<JsonArray>();
            Serial.print("[");
            for (int j = 0; j < innerArray.size(); j++) {{
                Serial.print(innerArray[j].as<float>(), 2); // Imprime solo 2 decimales
                if (j < innerArray.size() - 1) {{
                    Serial.print(", ");
                }}
            }}
            Serial.print("]");
            if (i < biArray.size() - 1) {{
                Serial.print(", ");
            }}
        }}
        Serial.println("]");
      }} else {{
        Serial.println("Error: Uno o más valores no son números flotantes.");
      }}
    }} else {{
      Serial.println("Error: El JSON recibido no cumple con el formato esperado.");
    }}
  }} else {{
    Serial.println("Error: El JSON recibido no cumple con el formato esperado.");
  }}
}}

// connects or reconnects to MQTT
// connects -> subscribes to topic and publishes a message (Commented)
// no -> waits 5 seconds
void ConnectMqtt()
{{
    Serial.print("Starting MQTT connection...");
    if (mqttClient.connect(MQTT_CLIENT_NAME))
    {{
        mqttClient.subscribe(receive_topic);
        Serial.println("Connected");
    }}
    else
    {{
        Serial.print("Failed MQTT connection, rc=");
        Serial.print(mqttClient.state());
        Serial.println(" try again in 5 seconds");

        delay(5000);
    }}
}}

void setup() {{
  Serial.begin(115200);
  wifiInit();
  mqttClient.setServer(server, port);
  mqttClient.setCallback(OnMqttReceived);
  while (!model.begin()) {{
    Serial.print("Error in NN initialization: ");
    Serial.println(model.getErrorMessage());
  }}
  ArduinoOTA.begin();  // Starts OTA
}}

void loop() {{
  if (!mqttClient.connected()) {{
    ConnectMqtt();
  }}
  ArduinoOTA.handle();  // Handles a code update request
  mqttClient.loop();
}}
'''
    return codigo_arduino












def generar_codigo_arduino():
  codigo_arduino = f'''
#include <ArduinoOTA.h>  // For enabling over-the-air updates
#include <WiFi.h>        // For connecting ESP32 to WiFi

char* ssid     = "vodafoneC080";
char* password = "JoSE.carCHEleJO.arBOL";


#include<Arduino.h>

#define LED 2


void setup() {{
Serial.begin(115200); // SERIAL BAUD RATE
pinMode(LED, OUTPUT);
WiFi.begin(ssid, password);  // Connect to WiFi - defaults to WiFi Station mode

// Ensure WiFi is connected
while (WiFi.status() != WL_CONNECTED) {{
    delay(500);
}}

ArduinoOTA.begin();  // Starts OTA
}}


// the loop function runs over and over again forever
void loop() {{
digitalWrite(LED, HIGH);  //LED PIN SET HIGH
Serial.println("LED ON"); // LED TURN ON
delay(1000);              // 1 SEC DELAY
digitalWrite(LED, LOW);   //LED PIN SET LOW
Serial.println("LED OFF"); // LED TURN OFF
delay(1000);               // 1 SEC DELAY
ArduinoOTA.handle();  // Handles a code update request
}}
    '''

  return codigo_arduino





#recibe un mensaje por un topico y reenvia ese mensaje por otro topico
def prueba(ssid, password, mqtt_client_name, server, port, receive_topic, send_topic):
  codigo_arduino = f'''
#include <WiFi.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "model.h"

WiFiClient esp32Client;
PubSubClient mqttClient(esp32Client);

char ssid[] = "{ssid}";
char password[] = "{password}";
char MQTT_CLIENT_NAME[] = "{mqtt_client_name}";
char server[] = "{server}";
int port = {port};
char receive_topic[] = "{receive_topic}";
char send_topic[] = "{send_topic}";



String receivedMessage = "";

const int MAX_JSON_SIZE = 512; // Tamaño máximo del JSON
const int MAX_VALUES = 20;     // Número máximo de valores que podemos almacenar

// Definir el tamaño de la matriz para almacenar múltiples valores de temperatura y humedad
const int NUM_READINGS = 24;
float readings[NUM_READINGS][2]; // [indice][0] para temperatura, [indice][1] para humedad


void printReadings() {{
  for (int i = 0; i < NUM_READINGS; i++) {{
    Serial.print("Temperatura ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(readings[i][0]);
    Serial.print("Humedad ");
    Serial.print(i);
    Serial.print(": ");
    Serial.println(readings[i][1]);
  }}
}}



void wifiInit() {{
  Serial.print("Conectándose a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {{
    Serial.print(".");
    delay(500);
  }}
  Serial.println("");
  Serial.println("Conectado a WiFi");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());
}}


void sendText(const char* text) {{
  mqttClient.publish(send_topic, text);
}}

void OnMqttReceived(char *topic, byte *payload, unsigned int length)
{{
    Serial.print("Received on ");
    Serial.print(topic);
    Serial.print(": ");

    // Extract the received text
    String receivedText = "";
    for (int i = 0; i < length; i++) {{
        receivedText += (char)payload[i];
    }}

    Serial.println(receivedText); // Print received text to serial monitor
    
    // Send the received text to the "send" topic
    sendText(receivedText.c_str());
}}



void ConnectMqtt()
{{
    Serial.print("Starting MQTT connection...");
    if (mqttClient.connect(MQTT_CLIENT_NAME))
    {{
        mqttClient.subscribe(receive_topic);
        Serial.println("Connected");
        //mqttClient.publish("connected","Entrada/01");
    }}
    else
    {{
        Serial.print("Failed MQTT connection, rc=");
        Serial.print(mqttClient.state());
        Serial.println(" try again in 5 seconds");

        delay(5000);
    }}
}}

void setup() {{
  Serial.begin(115200);
  delay(10);
  wifiInit();
  mqttClient.setServer(server, port);
  mqttClient.setBufferSize(1024); // SÚPER IMPORTANTE!!!!!!!!!!!!!!!!!!!!
  mqttClient.setCallback(OnMqttReceived);

  // Inicializar los valores a 0
  for (int i = 1; i < NUM_READINGS; i++) {{
  readings[i][0] = 0;
  readings[i][1] = 0;
  }}
}}

void loop() {{
  if (!mqttClient.connected()) {{
    ConnectMqtt();
  }}
  mqttClient.loop();
}}

    '''

  return codigo_arduino
