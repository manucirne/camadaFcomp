
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Aplicação
####################################################

print("comecou")

from enlace import *
from enlaceRx import *
from enlaceTx import *
import time
import binascii

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal:
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/tty.usbmodem1421"   # Mac    (variacao de)
#serialName = "COM7"                   # Windows(variacao de)



print("porta COM aberta com sucesso")



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

    #verificar que a comunicação foi aberta
    print("comunicação aberta")

  
    # Atualiza dados da transmissão
    txSize = com.tx.getStatus()
   

    # Faz a recepção dos dados
    print ("Recebendo dados .... ")
    bytesSeremLidos=com.rx.getBufferLen()
  
    tipo = 0
    npacoteesperado = 1
    rxBufferDF = b''

    while tipo == 0:   
        rxBuffer, nRx, erro = com.getData()
        if len(rxBuffer) > 0:
            tipo = rxBuffer[5]

    # print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")
    # print("rxBuffer: ", rxBuffer)
    # print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")



    end = bytes([1,2,3,4,5])
    stuffing = bytes(1)
    
    while tipo != 7:
        if tipo == 1:
            tipo = 2
            txBuffer0, npacote0 = empacotamento(bytes(1), 1, end, stuffing, tipo,1)
            while tipo != 3:
                com.sendData(txBuffer0)
                rxBuffer, nRx, erro = com.getData()
                if len(rxBuffer) > 0:
                    tipo = rxBuffer[5]
                if erro:
                    tipo = 1
                
        if tipo == 3:
            while tipo != 4:
                rxBuffer, nRx, erro = com.getData()
                if len(rxBuffer) > 5:
                    tipo = rxBuffer[5]
                
            #print("Tipo (4):             ", tipo)
        if tipo == 4:
            #print("Tipo (4):             ", tipo)
            #print("Pacote esperado:       ", npacoteesperado)
            rxBufferD, inicioEOP, tipo, npacote, pacoteatual = desempacotamento(rxBuffer, end, stuffing, npacoteesperado)
            
            #print("lenBuffer", len(rxBuffer))
            
            print("Tipo (5,6, 7 ou 8):             ", tipo)
            if tipo == 5:
                txBuffer, npacote0 = empacotamento(bytes(1), 1, end, stuffing, tipo,pacoteatual)
                com.sendData(txBuffer)  
                if (pacoteatual <= npacote):
                    tipo = 3
                    npacoteesperado += 1
                    rxBufferDF += rxBuffer[8:inicioEOP+1]
                    print("rxBufferD:::::::::::::::::", rxBufferDF)
                if pacoteatual == npacote:
                    with open("recebida.png", "wb+") as imageFile:
                        imagemrecebida = imageFile.write(rxBufferDF)
                    print("Tamanho total:      ", len(rxBuffer))
                    tipo = 7   
                                     
        if tipo == 6:
            print("Erro no recebimento - 6            " , tipo)
            txBuffer, npacote0 = empacotamento(bytes(1), 1, end, stuffing, tipo, 1)
            tipo = 3
            com.sendData(txBuffer)
        if tipo == 8:
            print("Erro no recebimento do pacote - 8            " , tipo)
            txBuffer, npacote0 = empacotamento(bytes(1), 1, end, stuffing, tipo, npacoteesperado)
            tipo = 3
            com.sendData(txBuffer)
        if tipo == 9:
            print("Erro de CRC            " , tipo)
            txBuffer, npacote0 = empacotamento(bytes(1), 1, end, stuffing, tipo, npacoteesperado)
            tipo = 3
            com.sendData(txBuffer)

    
    
    print("Mensagem recebida corretamente             ", tipo)
    txBuffer,npacote0 = empacotamento(bytes(1), 1, end, stuffing, tipo,1)
    com.sendData(txBuffer)

    


    # log
    print ("Lido              {} bytes ".format(rxBuffer[8:inicioEOP+1])) 
    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")
    print ("rxBuffer apos retirada: ", rxBuffer)
    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")


    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()


    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
