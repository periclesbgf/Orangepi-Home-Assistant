from paho.mqtt.client import CallbackAPIVersion
from paho.mqtt.client import MQTTv311
import paho.mqtt.client as mqtt
import ssl


from constants import MQTT_BROKER, MQTT_PORT, MQTT_TOPIC, CA_CERTIFICATE, CLIENT_CERTIFICATE, CLIENT_PRIVATE_KEY

def on_message(client, userdata, msg):
    print(f"Received message: {msg.topic} {str(msg.payload)}")

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code {rc}")
    if rc == 0:
        client.subscribe(MQTT_TOPIC)
    else:
        print(f"Failed to connect, return code {rc}\n")

def mqtt_publish(message, topic):
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)  # Assumindo a utilização do protocolo MQTT v3.1.1

    # Defina sua função on_connect aqui
    client.on_connect = on_connect

    # Configura a conexão TLS
    client.tls_set(ca_certs=CA_CERTIFICATE,
                   certfile=CLIENT_CERTIFICATE,
                   keyfile=CLIENT_PRIVATE_KEY,
                   tls_version=ssl.PROTOCOL_TLSv1_2)

    # Conecta ao broker MQTT
    client.connect(MQTT_BROKER, MQTT_PORT, 60)

    # Inicia um loop em background para gerenciar a conexão
    client.loop_start()

    # Publica a mensagem e captura o resultado em info
    info = client.publish(topic, message)

    # Aguarda a conclusão do envio da mensagem
    info.wait_for_publish()

    # Log do resultado da publicação
    print(f"Message published: MID={info.mid}, Granted QoS={info.rc}")

    # Para a execução do loop e desconecta do broker
    client.loop_stop()
    client.disconnect()


def initialize_mqtt_client():
    client = mqtt.Client(callback_api_version=CallbackAPIVersion.VERSION2)

    # Configure TLS connection
    client.tls_set(ca_certs=CA_CERTIFICATE,
                   certfile=CLIENT_CERTIFICATE,
                   keyfile=CLIENT_PRIVATE_KEY,
                   tls_version=mqtt.ssl.PROTOCOL_TLS)

    # Assign event callbacks
    client.on_connect = on_connect
    client.on_message = on_message

    # Parse MQTT_BROKER to remove "mqtts://" and extract the host
    mqtt_broker_host = MQTT_BROKER.replace("mqtts://", "").split(":")[0]

    # Connect to MQTT broker
    client.connect(mqtt_broker_host, MQTT_PORT, 60)

    return client