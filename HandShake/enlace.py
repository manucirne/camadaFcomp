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

# Construct Struct
#from construct import *

# Interface Física
from interfaceFisica import fisica

# enlace Tx e Rx
from enlaceRx import RX
from enlaceTx import TX

class enlace(object):
    """ This class implements methods to the interface between Enlace and Application
    """

    def __init__(self, name):
        """ Initializes the enlace class
        """
        self.fisica      = fisica(name)
        self.rx          = RX(self.fisica)
        self.tx          = TX(self.fisica)
        self.connected   = False

    def enable(self):
        """ Enable reception and transmission
        """
        self.fisica.open()
        self.rx.threadStart()
        self.tx.threadStart()

    def disable(self):
        """ Disable reception and transmission
        """
        self.rx.threadKill()
        self.tx.threadKill()
        time.sleep(1)
        self.fisica.close()

    ################################
    # Application  interface       #
    ################################
    def sendData(self, data):
        """ Send data over the enlace interface
        """
        tipo = 1
        data = data
        dataR = data
        resposta = False
        while not resposta:
            if tipo == 1:
                self.tx.sendBuffer(data, 1)
                data, tipobyte = self.rx.getNData()
                tipo = int.from_bytes(tipobyte, byteorder="big")
                print("tipo 1")
            if tipo == 2:
                print("tipo 2")
                self.tx.sendBuffer(data, 3)
                resposta = True
                time.sleep(1)                
                

        resposta = False

        while not resposta:
            self.tx.sendBuffer(dataR, 4)
            data, tipo = self.rx.getNData()
            tipo = int.from_bytes(tipo, byteorder="big")
            if tipo == 5:
                print("Mensagem enviada corretamente")
                print("Tipo 5")
                tipo = 7
                resposta = True

            if tipo == 6:
                print("Erro na mensagem - tipo 6")
                print("Reiniciando")



    def getData(self): #, size):
        """ Get n data over the enlace interface
        Return the byte array and the size of the buffer
        """
        # print('entrou na leitura e tentara ler ' + str(size) )
        
        resposta = False

        while not resposta:
            data, tipo = self.rx.getNData()
            tipo = int.from_bytes(tipo, byteorder="big")
            if tipo == 1:
                self.tx.sendBuffer(data, 2)
            if tipo == 3:
                resposta = True

        resposta = False
        while not resposta:
            data, tipo = self.rx.getNData()
            if tipo == 5:
                self.tx.sendBuffer(data, 5)
                print("Mensagem recebida corretamente")
                resposta = True 
            if tipo == 6:
                self.tx.sendBuffer(data, 6)
                print("Erro na mensagem - tipo 6")
 

       
        return(data, len(data))
