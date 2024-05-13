import machine    
from   MQTT              import *
from   ESP_CONNECTION    import *
from   GALGADEPESO       import *
from   SENSORTEMPERATURA import *
from   time              import sleep
from   machine           import Timer
from   machine           import Pin, PWM


_BROKER               = "62.171.140.128"
_CLIENT_ID            = "IncubadoraClient"

ZERO_CROSS_PIN_NUMBER = 12
ACD_PIN_NUMBER        = 2
MIN_POWER             = 5
MAX_POWER             = 100


is_dimmer_on          = True
zero_cross_pin        = Pin(ZERO_CROSS_PIN_NUMBER, Pin.IN)
acd_pin               = PWM(Pin(ACD_PIN_NUMBER), freq=1000)

             
SENSOR_PESO           = GalgaPeso(32)
_TARA                 = SENSOR_PESO.CalibrarTara()
SENSOR_TEMP           = SensorTemperatura(35)



global CERO, SETCONTROL , SETTEMP , _CRUCEPORCERO , _ANGREAL ,_anguloDisparo



def toggle_dimmer(state):
    
    global is_dimmer_on
    
    if state == "OFF":
        acd_pin.duty(0) 
        print("Dimmer apagado.")
        is_dimmer_on = False
        
    else:
        acd_pin.duty(1023) 
        print("Dimmer encendido.")
        is_dimmer_on = True

def adjust_power(power_level):
    
    duty_cycle     = int((power_level / 100) * 1023)
    acd_pin.duty(duty_cycle)
    print(f"Potencia ajustada al {power_level}%")




def set_action(_msg):
    global CERO , SETCONTROL, SETTEMP
    
    
    if "'VariablesIncubadora/PESO/CERO': true" in _msg:
        CERO        = SENSOR_PESO.getMedidaPeso(_TARA)
    if "'VariablesIncubadora/TEMPERATURA/CONTROL': true" in _msg:
        SETCONTROL  = 1
    if "'VariablesIncubadora/TEMPERATURA/CONTROL': false" in _msg:
        SETCONTROL  = 0
    if "'VariablesIncubadora/TEMPERATURA/SETPOINT'" in _msg:
        try:
            SETTEMP = float(_msg.split(":")[1].strip().strip("'"))
            print("Setpoint actualizado a:", SETTEMP)
        except ValueError:
            print("Error al convertir el setpoint a número.")
    


def message_callback(topic, msg):
    topic     = topic.decode()
    msg       = msg.decode()
    mes_      = f"'{topic}': {msg}"
    set_action(mes_)



def run():
    
    global CERO , SETCONTROL , SETTEMP , _CRUCEPORCERO , _ANGREAL , _anguloDisparo
    
    
    SETCONTROL        = 0
    CERO              = 0
    SETTEMP           = 0
    _KD               = 10 
    _KI               = 0.1
    _KP               = 20
    _CRUCEPORCERO     = False
    _ANGREAL          = 0
    
    ERROR_ANT         = 0
    ERROR             = 0
    ERROR_DERIVATIVO  = 0
    ERROR_SUMA        = 0
    _anguloDisparo    = 0   
    ERROR_ANT         = 0
    TIEMPO_ANT        = 0
    TIEMPO_ATC        = 0


    toggle_dimmer("ON")
    
     
    wifi = ESP32_CONNECTION()
    if wifi.status():
        print("Ya está conectado")
    else:
        if not wifi.connect():
            print("Falló la conexión WiFi")
            return

    
    client = MQTTClient(client_id=_CLIENT_ID, server=_BROKER)
    client.set_callback(message_callback)

    try:
        client.connect()
        client.subscribe("VariablesIncubadora/PESO/CERO",            qos=1)
        client.subscribe("VariablesIncubadora/TEMPERATURA/CONTROL",  qos=1)
        client.subscribe("VariablesIncubadora/TEMPERATURA/SETPOINT", qos=1)
        print("Subscrito")
    except Exception as e:
        print("Error conectando al broker MQTT o suscribiendo al tópico:", e)
        return


    try:
        while True:
            try:
                
                power_input  = _anguloDisparo
                dimmer_value = (power_input / 100) * (MAX_POWER - MIN_POWER) + MIN_POWER
                
            
                if dimmer_value == 0:
                    toggle_dimmer("OFF")
                else:
                    adjust_power(dimmer_value)
                    
               
                _peso             = SENSOR_PESO.getMedidaPeso(_TARA) - CERO
                _temp             = SENSOR_TEMP.getMedidaTemperatura()
                
                ERROR             = SETTEMP - _temp
                ERROR_DERIVATIVO  = ERROR - ERROR_ANT
                ERROR_SUMA        += (_KI*ERROR)
                _anguloDisparo    = ((_KP*ERROR) + (ERROR_SUMA) + (_KD*ERROR_DERIVATIVO))
                
                if(_anguloDisparo >= 99):
                    _anguloDisparo = 98
                if(_anguloDisparo <= 0 ):
                    _anguloDisparo = 0

                
                ERROR_ANT         = ERROR
                TIEMPO_ANT        = TIEMPO_ATC
                
                
                print("-------------------------------------")
                print(f"El peso es          ->       {_peso}") 
                print(f"la temperatura es   ->       {_temp}")
                print(f"% Valor de potencia -> {power_input}")
                print("-------------------------------------")
                
                
                client.publish("VariablesIncubadora/PESO"       , str(_peso))
                client.publish("VariablesIncubadora/TEMPERATURA", str(_temp))
                
            except Exception as e:
                print("Error MQTT al publicar:", e)
            client.check_msg()  
            sleep(0.1)
    finally:
        client.disconnect()
        acd_pin.deinit()
        
        


if __name__ == "__main__":
    run()
