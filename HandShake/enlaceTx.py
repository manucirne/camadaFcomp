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
from aplicacaoenvia import *

#Variáveis Protocolo
end = bytes([1,2,3,4,5])
stuffing = bytes(1)

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

    def sendBuffer(self, data, tipo):
        """ Write a new data to the transmission buffer.
            This function is non blocked.

        This function must be called only after the end
        of transmission, this erase all content of the buffer
        in order to save the new value.
        """

        
        baudrate = 115200
        
        txLen, tamanhoEmByte, payload =  self.empacotamento(data, end, stuffing, tipo)

        deltaT = (10)*txLen/baudrate

        vazios = bytes(5)
        tipoDeMensagem = bytes([tipo])
        head = vazios + tipoDeMensagem + tamanhoEmByte
        txBuffer =  head + payload + end
        overhead = len(payload)/len(txBuffer)
        throughput = len(payload)/deltaT

        self.transLen   = 0
        self.buffer = data
        self.threadMutex  = True
        

        print("-------------------------") 
        print("Throughput:       ", throughput,"bytes/s")
        print("OverHead:         ", overhead, "%") 
        print("Head: ",head)
        print("Stuffing: ",stuffing)
        print("EOF: ",end)
        print("-------------------------")

        return tipoDeMensagem

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


    def empacotamento(self,data,end, stuffing, tipo):
        #HEAD
    #tamanhoEmByte = bytes([txLen]) 
        
        txLen = len(data) 
        txBuffer = data 
        if tipo == 1:
            txBuffer = bytes(1)
        elif tipo == 2:
            txBuffer = bytes(1)
        elif tipo == 3:
            txBuffer = bytes(1)
        elif tipo == 4:
            for i in range(txLen): 
                data = txBuffer[i:]
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
        print("txLen: ",txLen)
        tamanhoEmByte = (txLen).to_bytes(2,byteorder='big')
        

        return txLen, tamanhoEmByte, txBuffer



