arduino_code = ""

def set_arduino_code(new_value):
    global arduino_code
    arduino_code = new_value

def get_arduino_code():
  return arduino_code

def set_arduino_code_template(ssid, password, mqtt_client_name, server, port, receive_topic, send_topic):
    global arduino_code

    arduino_code = f'''
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
