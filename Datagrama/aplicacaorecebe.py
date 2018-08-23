
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
import time
import binascii

# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
serialName = "/dev/tty.usbmodem1411"   # Mac    (variacao de)
#serialName = "COM5"                   # Windows(variacao de)



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

    print("rxBuffer: ", rxBuffer)

    end = bytes([1,2,3,4,5])
    stuffing = bytes(1)


    for i in range(8, len(rxBuffer)-1): 
        if bytes(rxBuffer[i+1:i+6]) == end:
            print("entrou no if 1")

            if  bytes([rxBuffer[i-1]]) == stuffing and bytes([rxBuffer[i+6]]) == stuffing:
                print("entrou no if 2")
                zero1 = i
                zero2 = i+6
                rxBuffer = rxBuffer[:zero1] + rxBuffer[zero1+1:zero2] + rxBuffer[zero2+1:]

            else:
                print("Encontramos o fim!! :)")
                print(i-7)




    with open("recebida", "wb+") as imageFile:
        imagemrecebida = imageFile.write(rxBuffer)

    # log
    print ("Lido              {} bytes ".format(nRx))
    
    print ("rxBuffer apos retirada: ", rxBuffer)

    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
