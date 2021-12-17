from bitarray import bitarray

from Random import Random
import random


def cyclic_redundancy_check(filename: str, divisor: str, len_crc: int) -> int:
    """
    This function computes the CRC of a plain-text file 
    arguments:
    filename: the file containing the plain-text
    divisor: the generator polynomium
    len_crc: The number of redundant bits (r)
    """
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
        
"""
Prueba del funcionamiento de la función cyclic_redundacy_check
http://www.sunshine2k.de/coding/javascript/crc/crc_js.html
"""

def make_binary_message(filename :str,divisor: str, len_crc: int)->bitarray:
    from bitarray import bitarray    
    bin_file = bitarray()
    with open(filename, 'rb') as file:
        bin_file.fromfile(file)

    #print('bin_file ', bin_file)
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
    MT19937 = Random(9) #semilla que en MT
    var = MT19937.randint(0,len_data-10)
    return var

def generadorErrores(n:int,message:int)->int:  
    #myAleatorio indica donde comezara la rfaga de error
    myAleatorio=aleatorio(len(message))#304 
    newMessage=bitarray(message)
     
    for i in range (myAleatorio,myAleatorio+n):
        
        if(i==myAleatorio or i==myAleatorio+n):#inicio y fin de la rafaga de error
            newMessage[i]=not newMessage[i]
        else:
            if(random.randint(0,2)==1):#de forma aleatoria el relleno de la 
                                       #rafaga se invierte
                newMessage[i]=not newMessage[i]
        
    return (newMessage)

def burst_error(msg:bitarray, n:int, seed: int)->bitarray:
    #random.seed(seed)
    start =random.randint(0,len(msg)-n)
    msg[start] ^= 1
    msg[start+n-1] ^= 1
    for i in range (start+1,start+n-1):
        if random.random() > 0.5:
            msg[i] ^= 1
    return msg

"""def generadorErrores(n:int,message:int)->int:  
   # print(message[304:308])
    myAleatorio=aleatorio(len(message))#304
    
    newMessage=bitarray(message)
     
    for i in range (myAleatorio,myAleatorio+n):
        MT19937 = Random(7)#random.randint(0,9999)) 
        
        if(random.randint(0,2)==1):
            newMessage[i]=not newMessage[i]
        
    return (newMessage)"""
    

def validador():
    detectadosP1=0
    igualesP1=0

    detectadosP2=0
    igualesP2=0

    detectadosP3=0
    igualesP3=0

    crc=cyclic_redundancy_check('test.txt', '10111', 4)   
    c=make_binary_message('test.txt', '10111', 4)

    for i in range (0,1000):
        n=4
        new=bitarray(c)
        ErrorMesage=burst_error(new,n,4)#n , message
        if (decoder(ErrorMesage,'10111',crc)==False):
            detectadosP1= detectadosP1+1
        else:
            if(ErrorMesage==c):
                igualesP1=igualesP1+1

    print ("Errores detectados con n=",n,": ",detectadosP1)
    print ("message no modificados n=",n,": ",igualesP1)
    noDetectados=1000-(detectadosP1+igualesP1)
    print ("Errores no detectados: ",noDetectados)
    print ("Errores que fec no detecto ",str(noDetectados*100/(detectadosP1+noDetectados))+"%\n") 
    for i in range (0,1000):
        n=5
        new=bitarray(c)
        ErrorMesage=burst_error(new,n,69)#n , message
        if (decoder(ErrorMesage,'10111',crc)==False):
            detectadosP2= detectadosP2+1
        else:
            if(ErrorMesage==c):
                igualesP2=igualesP2+1

    print ("Errores detectados con n=",n,": ",detectadosP2)
    print ("message no modificados n=",n,": ",igualesP2)
    noDetectados=1000-(detectadosP2+igualesP2)
    print ("Errores no detectados: ",noDetectados)
    print ("Errores que fec no detecto ",str(float(noDetectados)*100/float((detectadosP2+noDetectados)))+"%\n") 
    

    for i in range (0,1000):
        n=6
        new = bitarray(c)
        ErrorMesage=burst_error(new,n,69)#n , message
        if (decoder(ErrorMesage,'10111',crc)==False):
            detectadosP3= detectadosP3+1
        else:
            if(ErrorMesage==c):
                igualesP3=igualesP3+1
    print ("Errores detectados con n=",n,": ",detectadosP3)
    print ("message no modificados n=",n,": ",igualesP3)
    noDetectados=1000-(detectadosP3+igualesP3)
    print ("Errores no detectados: ",noDetectados)
    print ("Errores que fec no detecto ",str(noDetectados*100/(detectadosP3+noDetectados))+"%\n") 



num=[1,2,3,4,5,6]
print(num[-2:len(num)])

crc=cyclic_redundancy_check('test.txt', '10111', 4)   
c=make_binary_message('test.txt', '10111', 4)

print (crc)
print (c)

print(decoder (c,'10111',crc))

validador()


