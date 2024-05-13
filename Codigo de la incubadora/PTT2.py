from machine import Pin, PWM


ZERO_CROSS_PIN_NUMBER = 12
ACD_PIN_NUMBER        = 2
MIN_POWER             = 0
MAX_POWER             = 100
is_dimmer_on          = True
zero_cross_pin        = Pin(ZERO_CROSS_PIN_NUMBER, Pin.IN)
acd_pin               = PWM(Pin(ACD_PIN_NUMBER), freq=1000)  


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

def main():
    
    print("ESP32 System")
    toggle_dimmer("ON")
    
    while True:
        try:
            power_input = int(input("Introduce el valor de potencia (0-100): "))
            print(f"% Valor de la lámpara -> {power_input}")
            dimmer_value = (power_input / 100) * (MAX_POWER - MIN_POWER) + MIN_POWER
            
            if dimmer_value == 0:
                toggle_dimmer("OFF")
            else:
                adjust_power(dimmer_value)
    
            
            
        except KeyboardInterrupt:
            print("Deteniendo el programa...")
            acd_pin.deinit()  
            print("Dimmer desactivado.")
            break
'''
if __name__ == "__main__":
    main()
'''