
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
#serialName = "COM8"                   # Windows(variacao de)



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

    while tipo == 0:   
        rxBuffer, nRx = com.getData()
        if len(rxBuffer) > 0:
            tipo = rxBuffer[5]

    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")
    print("rxBuffer: ", rxBuffer)
    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")



    end = bytes([1,2,3,4,5])
    stuffing = bytes(1)
    print("Tipo:             ", tipo)
    
    while tipo != 5 and tipo < 7:
        print("entrou no while")
        if tipo == 1:
            tipo = 2
            print("Tipo (2):             ", tipo)
            txBuffer0 = empacotamento(bytes(1), 1, end, stuffing, tipo)
            while tipo != 3:
                com.sendData(txBuffer0)
                rxBuffer, nRx = com.getData()
                tipo = rxBuffer[5]
            print("Tipo (3):             ", tipo)
        if tipo == 3:
            while tipo != 4:
                rxBuffer, nRx = com.getData()
                tipo = rxBuffer[5]
            print("Tipo (4):             ", tipo)
        if tipo == 4:
            print("Tipo (4):             ", tipo)
            rxBuffer, inicioEOP, tipo = desempacotamento(rxBuffer, end, stuffing)
            with open("recebida.png", "wb+") as imageFile:
                imagemrecebida = imageFile.write(rxBuffer[8:inicioEOP])
                print("rxBuffer.     ", rxBuffer)
            print("Tipo (6 ou 7):             ", tipo)
            if tipo == 5:
                tipo = 7
        if tipo == 6:
            print("Erro no recebimento - 6            " , tipo)
            tipo = 4
            txBuffer = empacotamento(bytes(1), 1, end, stuffing, tipo)
            com.sendData(txBuffer)
        print("Tipo:             ", tipo, "###############")


    
    
    print("Mensagem recebida corretamente             ", tipo)
    txBuffer = empacotamento(bytes(1), 1, end, stuffing, tipo)
    com.sendData(txBuffer)


    # log
    print ("Lido              {} bytes ".format(rxBuffer[8:inicioEOP])) 
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
