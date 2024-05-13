import machine
from   network import WLAN
import network
from   MQTT import MQTTClient
from   ESP_CONNECTION import *
from   SENSORTEMPERATURA import *
from   time import sleep

# Configuración de la conexión MQTT y del sensor
CLIENT_ID         = "TuristTechSTEAM"
AWS_ENDPOINT      = "a3qn905w11clf0-ats.iot.us-east-1.amazonaws.com"
keyfile           = '/Certificados/TuristTechSTEAM-private.pem.key'
certfile          = '/Certificados/TuristTechSTEAM-certificate.pem.crt'

SENSOR_TEMP       = SensorTemperatura(35)
pin               = machine.Pin(2, machine.Pin.OUT)

def read_certificates():
    
    """ Lee los certificados necesarios para la conexión SSL. """
    
    try:
        with open(keyfile, 'r') as f:
            key = f.read()
        with open(certfile, 'r') as f:
            cert = f.read()
        return {'key': key, 'cert': cert, 'server_side': False}
    
    except Exception as e:
        print(f"Error al leer los archivos de certificado: {e}")
        raise SystemExit

def setup_wifi():
    
    """ Configura y conecta a la red WiFi. """
    
    wifi = ESP32_CONNECTION()
    if not wifi.status():
        if not wifi.connect():
            print("Falló la conexión WiFi")
            raise SystemExit
        else:
            print("Conectado a WiFi")
    else:
        print("Ya está conectado a WiFi")


def setup_mqtt(ssl_params):
    
    """ Configura la conexión MQTT. """
    try:
        mqtt = MQTTClient(CLIENT_ID, AWS_ENDPOINT, port=8883, ssl=True, ssl_params=ssl_params)
        mqtt.connect()
        return mqtt
    except Exception as e:
        print(f"Error al conectar con MQTT: {e}")
        raise SystemExit

def set_action(_msg):
    if "TRUE" in _msg:
        pin.value(1)
    else:
        pin.value(0)

def subscribe_to_topics(mqtt):
    """ Configura las suscripciones a los tópicos MQTT. """
    
    def message_callback(topic, msg):
        topic = topic.decode()
        msg = msg.decode()
        print(f"Received message on topic '{topic}': {msg}")
        set_action(msg)
        
    
    mqtt.set_callback(message_callback)
    mqtt.subscribe("centrosteam/datosub", qos=1)

def run(mqtt):
    
    """ Bucle principal para publicar datos y comprobar mensajes. """
    
    _time = 1
    
    try:
        while True:
            _temp = SENSOR_TEMP.getMedidaTemperatura()
            
            
            if _time == 0:
                mensaje_json = '{{ "Temperatura": {} }}'.format(_temp)
                mqtt.publish(topic="centrosteam/datopub", msg=mensaje_json, qos=0)
                print("Mensaje enviado")
                _time = 1
    
                    
            mqtt.check_msg()
            _time = _time - 1
            
            sleep(1) 
    finally:
        mqtt.disconnect()
        print("Desconectado del broker MQTT.")

def main():
    
    ssl_params = read_certificates()
    setup_wifi()
    mqtt       = setup_mqtt(ssl_params)
    subscribe_to_topics(mqtt)
    run(mqtt)


'''
if __name__ == "__main__":
    main()
''' 

