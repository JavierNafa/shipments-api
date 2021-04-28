from enum import Enum

class Zone(str,Enum):
    urbano = 'Urbano'
    rural = 'Rural'
    semiurbano = 'Semiurbano'