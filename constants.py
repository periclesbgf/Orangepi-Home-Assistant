# MQTT
MQTT_BROKER = "a34ypir054ngjb-ats.iot.us-east-2.amazonaws.com"
MQTT_PORT = 8883
MQTT_TOPIC = "topic/esp32/pub"
CA_CERTIFICATE = "certs/AmazonRootCA1.pem"
CLIENT_CERTIFICATE = "certs/client.crt"
CLIENT_PRIVATE_KEY = "certs/client.key"

# Connections
#SERVER_IP = "192.168.1.12" # Your id: if windows ipconfig, linux: ifconfig
SERVER_PORT = 12445 # Server port
#ESP32_TCP_SERVER_IP = "192.168.1.15"  # Substitua pelo IP do servidor TCP da ESP32
ESP32_TCP_SERVER_PORT_FOR = 12345  # Substitua pela porta do servidor TCP da ESP32
RECEIVE_DURATION_SECONDS = 1
RECEIVE_DURATION_SECONDS_R = 3
RECEIVE_BUFFER_SIZE = 1024
SEND_BUFFER_SIZE = 2048

commands = ['background', 'eden']

wav_file_path = "./reformated2.wav"

