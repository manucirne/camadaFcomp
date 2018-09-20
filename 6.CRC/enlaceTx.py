#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
import threading


# Class
class TX(object):
    """ This class implements methods to handle the transmission
        data over the p2p fox protocol
    """

    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.transLen    = 0
        self.empty       = True
        self.threadMutex = False
        self.threadStop  = False


    def thread(self):
        """ TX thread, to send data in parallel with the code
        """
        
        while not self.threadStop:  
            if(self.threadMutex):
                Tinicio = time.time()
                self.transLen    = self.fisica.write(self.buffer)
                #print("O tamanho transmitido. IMpressao dentro do thread {}" .format(self.transLen))
                self.threadMutex = False
                Tfinal = time.time()
                deltaT = (Tfinal - Tinicio)
                txLen = len(self.buffer)
                baudrate = 115200
                
                print("-------------------------")
                print("Tempo Esperado:   ", (10)*txLen/baudrate,"s")
                print("Tempo Medido:     ", deltaT,"s") 
                print("-------------------------")

    def threadStart(self):
        """ Starts TX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill TX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the TX thread to run

        This must be used when manipulating the tx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the TX thread (after suspended)
        """
        self.threadMutex = True

    def sendBuffer(self, data):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """
        self.transLen   = 0
        self.buffer = data
        self.threadMutex  = True

    def getBufferLen(self):
        """ Return the total size of bytes in the TX buffer
        """
        return(len(self.buffer))

    def getStatus(self):
        """ Return the last transmission size
        """
        #print("O tamanho transmitido. Impressao fora do thread {}" .format(self.transLen))
        return(self.transLen)
        

    def getIsBussy(self):
        """ Return true if a transmission is ongoing
        """
        return(self.threadMutex)


def CRCenvia(payload):
    divisor = bin(int("49157", 10))[2:]
    zeros = bytes(len(divisor)-1)
    zerosDiv = bin(int("00000", 10))[2:]
    payload = payload + zeros
    payload = int.from_bytes(payload, byteorder='big', signed=False)
    payload = bin(payload)[2:]
    

    while len(payload) > len(divisor):
        if payload[0] == 1:
            payload = (divisor ^ payload[0:len(divisor)+1]) + payload[len(divisor)+1:]
        else:
            payload = (zerosDiv ^ payload[0:len(divisor)+1]) + payload[len(divisor)+1:]
        payload = payload[1:]
    return payload

        
def empacotamento(txBuffer, txLen, end, stuffing, tipo, pacoteatual): 
    if (tipo == 1) or (tipo == 2) or (tipo == 3):
        pacote = bytes(1)
    if (tipo == 4):
        for i in range(txLen): 
            if i < (len(txBuffer)-5):
                if txBuffer[i] == end[0]:
                    if txBuffer[i+1] == end[1]:
                        if txBuffer[i+2] == end[2]:
                            if txBuffer[i+3] == end[3]:
                                if txBuffer[i+4] == end[4]:
                                    zero = bytes([txBuffer[i-1]])
                                    s = bytes([txBuffer[i+5]])
                                    if (bytes([txBuffer[i-1]]) != stuffing) or (bytes([txBuffer[i+5]]) != stuffing):
                                        txBuffer = txBuffer[:i] + stuffing + end + stuffing + txBuffer[i+5:]

    txLen    = len(txBuffer)
    npacote = txLen//128
    if (txLen%128) != 0:
        npacote += 1

    #print("Npacote:         " , npacote)
    Pinicio = (pacoteatual-1)*128
    Pfinal = Pinicio+128
    if npacote != pacoteatual:
        pacote = txBuffer[Pinicio:Pfinal]
        #print("Pacote                  ", pacote)
    else:
        pacote = txBuffer[Pinicio:]

    resto = CRCenvia(pacote)
    #print("txLen: ",txLen)
    #print("tamanho pacote atual: ",len(pacote))
    tamanhoEmByte = (len(pacote)).to_bytes(2,byteorder='big')
    pacoteatualBytes =(pacoteatual).to_bytes(1,byteorder='big')
    npacoteBytes =(npacote).to_bytes(1,byteorder='big')
    resto = (int(resto)).to_bytes(2,byteorder='big')
    vazio = bytes(1)
    tipo = bytes([tipo])

    
    head = vazio + resto + pacoteatualBytes + npacoteBytes  + tipo + tamanhoEmByte
    #print("HEAD:        ", head)

    payload = pacote
    txBuffer = head + payload + end
    #print("TXBUFFER NO EMPACOTAMENTO:    ", txBuffer)
    overhead = len(payload)/len(txBuffer)
    #throughput = payload/deltaT

    print("-------------------------")
    print("OverHead:     ", overhead, "%")
    print("Tipo:              ", tipo)
    #print("Throughput:       ", throughput,"bytes/s") 
    print("Head: ",head)
    print("Stuffing: ",stuffing)
    print("EOF: ",end)
    print("Número de pacotes:         " , npacote)
    print("Pacote atual:         " , pacoteatual)
    print("-------------------------")

    return txBuffer, npacote


