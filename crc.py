from bitarray import bitarray
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


def burst_error(msg:bitarray, n:int)->bitarray:
    start =random.randint(0,len(msg)-n)
    msg[start] ^= 1
    msg[start+n-1] ^= 1
    for i in range (start+1,start+n-1):
        if random.random() > 0.5:
            msg[i] ^= 1
    return msg
    

def validador():
    crc=cyclic_redundancy_check('test.txt', '10111', 4)   
    message=make_binary_message('test.txt', '10111', 4)

    for n in range(4,7):
        ErrorDetected=0
        for i in range (0,1000):
            new = bitarray(message)
            ErrorMesage=burst_error(new,n)#message, n
            if (decoder(ErrorMesage,'10111',crc)==False):
                ErrorDetected= ErrorDetected+1
        print ("Errores detectados con n=", n,": ",str(ErrorDetected*100/1000)+"%")

validador()
