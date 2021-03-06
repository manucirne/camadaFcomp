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

# Variaveis Protocolo
end = bytes([1,2,3,4,5])
stuffing = bytes(1)
EOP_encontrado = False

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
        print("entrou no getBuffer")
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        
        EOP_encontrado, b, inicioEOP, tamanho_esperado, tamanho_recebido, tipo = b.desempacotamento()

        self.threadResume()
        return (b, tipo)

    def getNData(self):
        """ Read N bytes of data from the reception buffer

        This function blocks until the number of bytes is received
        """
#        temPraLer = self.getBufferLen()
#        print('leu %s ' + str(temPraLer) )
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        
        x = self.getBufferLen()
        time.sleep(1)
        
        #if self.getBufferLen() < size:
            #print("ERROS!!! TERIA DE LER %s E LEU APENAS %s", (size,temPraLer))
        while((self.getBufferLen() == 0) or (self.getBufferLen() != x)):
            time.sleep(1)
            print("lenbuffer:   ",x)
            x = self.getBufferLen()
            time.sleep(1)
        print("saiu do while")
        b, tipo = self.getBuffer(x)
#      
        #self.buffer = self.desempacotamento()[1]
       # tipo = self.desempacotamento()[5]

        print("tipo", tipo)

        return(b, tipo)


    def clearBuffer(self):
        """ Clear the reception buffer
        """
        self.buffer = b""

    def desempacotamento(self):
        global end, stuffing, EOP_encontrado
        cont_s = 0
        print("self.buffer:      ",   self.buffer)
        tipo = self.buffer[5]
        tamanho_esperado = int.from_bytes(self.buffer[6:8], byteorder="big")

        print("tipo", tipo)
        if tipo == bytes([4]):
            print("tipo", tipo)
     
            for i in range(8, len(self.buffer)-1): 

                if bytes(self.buffer[i+1:i+6]) == end:

                    if  bytes([self.buffer[i-1]]) == stuffing and bytes([self.buffer[i+6]]) == stuffing:
                        cont_s += 2
                        zero1 = i
                        zero2 = i+6
                        self.buffer = self.buffer[:zero1] + self.buffer[zero1+1:zero2] + self.buffer[zero2+1:]

                    else:
                        tamanho_recebido = i-7+cont_s
                        print("Tamanho Informado no Head:    ", tamanho_esperado)
                        print("Tamanho da mensagem recebida: ", tamanho_recebido)
                        inicioEOP = i
                        print("Posição de início do EOP:     ",inicioEOP)
                        print("Encontramos o fim!! :)")
                        EOP_encontrado = True
                        if tamanho_esperado == tamanho_recebido:
                            tipo = 5
                        else:
                            tipo = 6
            
        else:
            if tipo == 1:
                EOP_encontrado = False
                inicioEOP = "null"
                tamanho_recebido = 1
                tipo = 2

        print("tipo", tipo)
        erros(tamanho_esperado,tamanho_recebido,EOP_encontrado)
        return EOP_encontrado, self.buffer, inicioEOP, tamanho_esperado, tamanho_recebido, tipo
            


    def erros(tamanho_esperado,tamanho_recebido):
        global EOP_encontrado
        if tamanho_esperado != tamanho_recebido:
            print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
            print("ERRO!! Número de bytes no payload não corresponde ao informado no head.")
            print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

        if not EOP_encontrado:
            print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
            print("ERRO!! O EOP não foi localizado.")
            print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
