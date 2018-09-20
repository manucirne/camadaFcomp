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
import numpy as np
# Threads
import threading
from PyCRC.CRC16 import CRC16


# Class
class RX(object):
    """ This class implements methods to handle the reception
        data over the p2p fox protocol
    """
    
    def __init__(self, fisica):
        """ Initializes the TX class
        """
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        """ RX thread, to send data in parallel with the code
        essa é a funcao executada quando o thread é chamado. 
        """
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp
                    # if nRx < int.from_bytes(self.buffer[6:8], byteorder="big"):
                    #     self.buffer += rxTemp
                    # else:
                    #     self.buffer = rxTemp
                time.sleep(0.01)

    def threadStart(self):
        """ Starts RX thread (generate and run)
        """
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        """ Kill RX thread
        """
        self.threadStop = True

    def threadPause(self):
        """ Stops the RX thread to run

        This must be used when manipulating the Rx buffer
        """
        self.threadMutex = False

    def threadResume(self):
        """ Resume the RX thread (after suspended)
        """
        self.threadMutex = True

    def getIsEmpty(self):
        """ Return if the reception buffer is empty
        """
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        """ Return the total number of bytes in the reception buffer
        """
        return(len(self.buffer))

    def getAllBuffer(self, len):
        """ Read ALL reception buffer and clears it
        """
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        """ Remove n data from buffer
        """
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self):#, size):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
#         while(self.getBufferLen() < size):
#             time.sleep(0.05)
# #                 
#         return(self.getBuffer(size))
        x = self.getBufferLen()
        time.sleep(0.1)
        

        tInicial = time.time()
        tFinal = time.time()

        erro = False
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        while(((self.getBufferLen() == 0) or (self.getBufferLen() != x)) and tFinal - tInicial < 5 ):
            #print("Buffer:         ", self.buffer)
            tFinal = time.time()
            time.sleep(0.2)
            #print("Buffer:         ", self.buffer)
            #print("lenbuffer:   ",x)
            x = self.getBufferLen()
            #time.sleep(1)

        if tFinal - tInicial >= 5 :
            print("Erro de tempo excedido")
            erro = True
        x = self.getBufferLen()
        return(self.getBuffer(x), erro)


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""



def CRCrecebe(data: bytes):
    '''
    CRC-16-ModBus Algorithm
    '''
    resto = CRC16().calculate(data)
    print("Resto no CRC (calculado):       ", resto)

    return resto

def desempacotamento(rxBuffer, end, stuffing, npacoteesperado):
    tamanho_esperado = int.from_bytes(rxBuffer[6:8], byteorder="big")
    #print("rxBuffer:    ", rxBuffer)
    EOP_encontrado = False
    npacote = rxBuffer[4]
    print("-----------------------------------------------")
    print("Número de pacotes:           ", npacote)
    pacoteatual = rxBuffer[3]
    print("Pacote atual:          ", pacoteatual)
    print("-----------------------------------------------")
    cont_s = 0
    tipo = 1
    head = rxBuffer[:8]
    inicioEOP = 0
    rxBufferCRC = rxBuffer[8:-5]


    for i in range(8, len(rxBuffer)): 

        if bytes(rxBuffer[i+1:i+6]) == end:

            if  bytes([rxBuffer[i-1]]) == stuffing and bytes([rxBuffer[i+6]]) == stuffing:
                cont_s += 2
                zero1 = i
                zero2 = i+7
                rxBuffer = rxBuffer[:zero1] + rxBuffer[zero1+1:zero2] + rxBuffer[zero2+1:]

            else:
                tamanho_recebido = i-7+cont_s
                print("Tamanho Informado no Head:    ", tamanho_esperado)
                print("Tamanho da mensagem recebida: ", tamanho_recebido)
                inicioEOP = i
                print("Posição de início do EOP:     ", inicioEOP)
                print("Encontramos o fim!! :)")
                EOP_encontrado = True
                rxBuffer = rxBuffer[8:i+1]
                #if tamanho_esperado > 1:
                tipo = 5
    print("head:    ", head)
    resto = head[1:3]
    print("resto1:    ", resto)
    resto = int.from_bytes(resto, byteorder="big")
    print("resto int from bytes: -------------------  ", resto)
    print("Resto do CRC:     ", CRCrecebe(rxBufferCRC))
    print("RxBuffer:   ", rxBufferCRC)


    if resto != CRCrecebe(rxBufferCRC):          ############# RxBuffer???????????
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        print("ERRO!! Algum bit veio errado. CRC")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        tipo = 9


    elif npacoteesperado != pacoteatual:
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        print("ERRO!! Pacote esperado diferente de pacote recebido.")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        tipo = 8

    elif not EOP_encontrado:
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        print("ERRO!! O EOP não foi localizado.")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        tipo = 6

    elif tamanho_esperado != tamanho_recebido:
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        print("ERRO!! Número de bytes no payload não corresponde ao informado no head.")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        tipo = 6

    else:
        tipo = 5

    # tamanhoEmByte = (txLen).to_bytes(2,byteorder='big')
    # vazio = bytes(5)
    # tipo = bytes([tipo])
    # head = vazio + tipo + tamanhoEmByte

    # rxBuffer = head + rxBuffer[8:]

    return rxBuffer, inicioEOP, tipo, npacote, pacoteatual

