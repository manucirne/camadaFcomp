
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
serialName = "/dev/tty.usbmodem1421"   # Mac    (variacao de)
#serialName = "COM5"                   # Windows(variacao de)



print("porta COM aberta com sucesso")

def desempacotamento(rxBuffer,end,stuffing,EOP_encontrado):
    cont_s = 0
    for i in range(8, len(rxBuffer)-1): 

        if bytes(rxBuffer[i+1:i+6]) == end:

            if  bytes([rxBuffer[i-1]]) == stuffing and bytes([rxBuffer[i+6]]) == stuffing:
                cont_s += 2
                zero1 = i
                zero2 = i+6
                rxBuffer = rxBuffer[:zero1] + rxBuffer[zero1+1:zero2] + rxBuffer[zero2+1:]

            else:
                tamanho_recebido = i-7+cont_s
                print("Tamanho da mensagem recebida: ", tamanho_recebido)
                inicioEOP = i
                print("Posição de início do EOP:     ",inicioEOP)
                print("Encontramos o fim!! :)")
                EOP_encontrado = True
    return EOP_encontrado, rxBuffer, inicioEOP, tamanho_recebido

def erros(tamanho_esperado,tamanho_recebido,EOP_encontrado):
    if tamanho_esperado != tamanho_recebido:
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        print("ERRO!! Número de bytes no payload não corresponde ao informado no head.")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")

    if not EOP_encontrado:
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")
        print("ERRO!! O EOP não foi localizado.")
        print("#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#")


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


    end = bytes([1,2,3,4,5])
    stuffing = bytes(1)


    tamanho_esperado = int.from_bytes(rxBuffer[6:8], byteorder="big")
    EOP_encontrado = False


    print("Tamanho Informado no Head:    ", tamanho_esperado)

    EOP_encontrado, rxBuffer, inicioEOP, tamanho_recebido = desempacotamento(rxBuffer,end,stuffing,EOP_encontrado)


    with open("recebida.png", "wb+") as imageFile:
        imagemrecebida = imageFile.write(rxBuffer[8:inicioEOP])

    erros(tamanho_esperado,tamanho_recebido,EOP_encontrado)

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
