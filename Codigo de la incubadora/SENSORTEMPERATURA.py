from machine import Pin, ADC
from time import sleep  

class SensorTemperatura:
    
    def __init__(self, _PIN):
        self.adc = ADC(Pin(_PIN))
        self.adc.atten(ADC.ATTN_11DB)

    def _getMedidaVoltaje(self,_M):
        if _M < 3:
            raise ValueError("Se requieren al menos 3 muestras para realizar el promedio.")
        _sum = 0
        
        for _ in range(_M):
            _medida            = ((self.adc.read()) * (3.3 / 4095)) + 0.13
            _sum              += _medida
            sleep(0.2)
        
        _pr = round(_sum / _M, 2)
        
        return _pr 
             
        
    def getMedidaTemperatura(self):
        
        _voltaje       =   self._getMedidaVoltaje(6)
        _temperatura   =   round((77.8 * (_voltaje)) + 27.0, 2)
        _suma_temp     =   0.0
        
        for __ in range(3):
            _temperatura   =   round((5 + (91.39784946 * (_voltaje - 0.06))), 2)
            _suma_temp    +=   _temperatura
        
        return round((_suma_temp/3),0)
    

