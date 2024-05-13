from machine import Pin
import time

led1 = Pin(13, Pin.OUT)
led2 = Pin(14, Pin.OUT)
led3 = Pin(27, Pin.OUT)
led4 = Pin(25, Pin.OUT)
led5 = Pin(33, Pin.OUT)


pin1 = Pin(15, Pin.IN, Pin.PULL_UP)
pin2 = Pin(4, Pin.IN, Pin.PULL_UP)
pin3 = Pin(5, Pin.IN, Pin.PULL_UP)
pin4 = Pin(18, Pin.IN, Pin.PULL_UP)
pin5 = Pin(19, Pin.IN, Pin.PULL_UP)

pin_to_led = {
    pin1: led5,
    pin2: led4,
    pin3: led3,
    pin4: led2,
    pin5: led1
}
'''
while True:
    for pin, led in pin_to_led.items():
        if pin.value() == 0: 
            led.on()
        else:  
            led.off()
    time.sleep(0.1)  
'''