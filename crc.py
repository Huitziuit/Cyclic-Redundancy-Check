from bitarray import bitarray
from Random import Random
import random

def cyclic_redundancy_check(filename: str, divisor: str, len_crc: int) -> int:
    from bitarray import bitarray
    redundancy = len_crc * bitarray('0')
    bin_file = bitarray()
    p = bitarray(divisor)
    len_p = len(p)
    with open(filename, 'rb') as file:
        bin_file.fromfile(file)
    cw = bin_file + redundancy
    rem = cw[0 : len_p]
    end = len(cw)
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1 
            rem[-1] = cw[i]
    return rem[len_p-len_crc : len_p]
        
def make_binary_message(filename :str,divisor: str, len_crc: int)->bitarray:
    from bitarray import bitarray    
    bin_file = bitarray()
    with open(filename, 'rb') as file:
        bin_file.fromfile(file)
    return bin_file +cyclic_redundancy_check(filename, divisor, len_crc) 


def decoder(message: int, divisor: str, crc:int) -> bool:
    from bitarray import bitarray 
    len_crc=len(crc)
    texto=message[0:-len_crc]
    redundancy = crc
    bin_file = texto
    p = bitarray(divisor)
    len_p = len(p) 
    cw = bin_file + redundancy
    rem = cw[0 : len_p]
    end = len(cw)
    for i in range(len_p, end + 1):
        if rem[0]:
            rem ^= p
        if i < end:
            rem = rem << 1 
            rem[-1] = cw[i]
    correcto = len_crc * bitarray('0')
    if(rem[len_p-len_crc : len_p]==correcto):
        return True
    else:
        return False

        
def aleatorio(len_data)-> int:
    MT19937 = Random(9) 
    var = MT19937.randint(0,len_data-10)
    return var


def burst_error(msg:bitarray, n:int, seed: int)->bitarray:
    start =random.randint(0,len(msg)-n)
    msg[start] ^= 1
    msg[start+n-1] ^= 1
    for i in range (start+1,start+n-1):
        if random.random() > 0.5:
            msg[i] ^= 1
    return msg
    

def validador():
    detectadosP1=0
    detectadosP2=0
    detectadosP3=0

    crc=cyclic_redundancy_check('test.txt', '10111', 4)   
    message=make_binary_message('test.txt', '10111', 4)

    for i in range (0,1000):
        n=4
        new=bitarray(message)
        ErrorMesage=burst_error(new,n,4)#n , message
        if (decoder(ErrorMesage,'10111',crc)==False):
            detectadosP1= detectadosP1+1
    print ("Errores detectados con n=4: ",str(detectadosP1*100/1000)+"%")
    
    
    for i in range (0,1000):
        n=5
        new=bitarray(message)
        ErrorMesage=burst_error(new,n,69)#n , message
        if (decoder(ErrorMesage,'10111',crc)==False):
            detectadosP2= detectadosP2+1
    print ("Errores detectados con n=5: ",str(detectadosP2*100/1000)+"%")
    

    for i in range (0,1000):
        n=6
        new = bitarray(message)
        ErrorMesage=burst_error(new,n,69)#n , message
        if (decoder(ErrorMesage,'10111',crc)==False):
            detectadosP3= detectadosP3+1
    print ("Errores detectados con n=6: ",str(detectadosP3*100/1000)+"%")


validador()


