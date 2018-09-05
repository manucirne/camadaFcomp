
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
import time
import binascii

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal:
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1421"   # Mac    (variacao de)
serialName = "COM8"                   # Windows(variacao de)



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
  
        
    rxBuffer, nRx = com.getData()

    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")
    print("rxBuffer: ", rxBuffer)
    print(". . . . . . . . . . . . . . . . . . . . . . . . . . . ")

    tipo = int.from_bytes(rxBuffer[5], byteorder="big")
    end = bytes([1,2,3,4,5])
    stuffing = bytes(1)

    
    while tipo != 5:
        if tipo == 1:
            tipo = 2
            txBuffer = empacotamento(bytes(1), 1, end, stuffing, tipo)
            com.sendData(txBuffer)
            rxBuffer, nRx = com.getData()
            tipo = int.from_bytes(rxBuffer[5], byteorder="big")
        if tipo == 3:
            rxBuffer, nRx = com.getData()
            tipo = int.from_bytes(rxBuffer[5], byteorder="big")
        if tipo == 4:
            rxBuffer, inicioEOP, tipo = desempacotamento(rxBuffer, end, stuffing)
        if tipo == 6:
            print("Erro no recebimento - 6            " , tipo)
            txBuffer = empacotamento(bytes(1), 1, end, stuffing, tipo)
            com.sendData(txBuffer)

    print("Mensagem recebida corretamente             ", tipo)
    txBuffer = empacotamento(bytes(1), 1, end, stuffing, tipo)
    com.sendData(txBuffer)



    with open("recebida.png", "wb+") as imageFile:
        imagemrecebida = imageFile.write(rxBuffer[8:inicioEOP])


    # log
    print ("Lido              {} bytes ".format(nRx)) 
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
