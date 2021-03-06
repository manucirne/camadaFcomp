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

        
def empacotamento(txBuffer, txLen, end, stuffing): 
    for i in range(txLen): 
        if txBuffer[i] == end[0]:
            if txBuffer[i+1] == end[1]:
                if txBuffer[i+2] == end[2]:
                    if txBuffer[i+3] == end[3]:
                        if txBuffer[i+4] == end[4]:
                            zero = bytes([txBuffer[i-1]])
                            s = bytes([txBuffer[i+5]])
                            if (bytes([txBuffer[i-1]]) != stuffing) or (bytes([txBuffer[i+5]]) != stuffing):
                                txBuffer = txBuffer[:i] + stuffing + end + stuffing + txBuffer[i+5:]
    data = txBuffer

    txLen    = len(txBuffer)
    print("txLen: ",txLen)
    tamanhoEmByte = (txLen).to_bytes(8,byteorder='big')
    
    head = tamanhoEmByte

    payload = txBuffer
    txBuffer = head + txBuffer + end
    overhead = len(payload)/len(txBuffer)
    #throughput = payload/deltaT

    print("-------------------------")
    print("OverHead:     ", overhead, "%")
    #print("Throughput:       ", throughput,"bytes/s") 
    print("Head: ",head)
    print("Stuffing: ",stuffing)
    print("EOF: ",end)
    print("-------------------------")

    return txBuffer


