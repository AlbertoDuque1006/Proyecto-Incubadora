
from machine import Pin, ADC
from time    import *


class GalgaPeso():
    
    def __init__(self,_PIN):
        self.adc  = ADC(Pin(_PIN))
        self.adc.atten(ADC.ATTN_11DB)
        
    def _getMedidaVoltaje(self,_M):
        if _M < 3:
            raise ValueError("Se requieren al menos 3 muestras para realizar el promedio.")
        _sum = 0
        
        for _ in range(_M):
            _medida            = ((self.adc.read()) * (3.3 / 4095)) + 0.15
            _sum              += _medida
            sleep(0.2)
        
        _pr = round(_sum / _M, 2)
        
        return _pr 
        

    def CalibrarTara(self):
        
        _SUMATARA     = 0.0
        _INTERACIONES = 3
        for i in range(_INTERACIONES):
            _SUMATARA += self._getMedidaVoltaje(3)
            sleep(1)
        print("Sensor de peso calibrado")
        return round((_SUMATARA / _INTERACIONES),2)

    
    
    def getMedidaPeso(self,_TARA):
        
        _VOLTAGE     = self._getMedidaVoltaje(3)
        _PESO        = round(((_VOLTAGE - _TARA) * 1950),2)
        return round(_PESO,2) if _PESO >= 1 else 0.0
        
        
        
        
        
    




    


