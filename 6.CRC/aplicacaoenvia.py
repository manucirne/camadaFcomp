
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
from enlaceTx import *
from enlaceRx import *
import time
from tkinter import *
from PIL import ImageTk, Image
import os
import datetime


from tkinter.filedialog import askopenfilename, askopenfile
from tkinter.messagebox import showerror


fname = "null"


# voce deverá descomentar e configurar a porta com através da qual ira fazer a
# comunicaçao
# Serial Com Port
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem28" # Mac    (variacao de)
serialName = "COM15"                  # Windows(variacao de)



print("porta COM aberta com sucesso")


# Valores protocolo
end = bytes([1,2,3,4,5])
stuffing = bytes(1)


def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    

    #verificar que a comunicação foi aberta
    print("comunicação aberta")

    class Application:
        def __init__(self, master=None):
            self.master = Frame(master)
            self.master.pack()
            self.master["bg"] = ("lightblue")
            self.master.grid(sticky=W+E+N+S)
            self.master.rowconfigure(5, weight=1)
            self.master.columnconfigure(5, weight=1)

            self.msg = Label(self.master, text="Primeira janela")
            self.msg["font"] = ("Verdana", "20")
            self.msg["bg"] = ("lightblue")
            self.msg.pack()

            self.button = Button(self.master, text="Browse", command=self.load_file, width=10)

            self.button.bind("<Button-1>", self.load_file)
            self.button.pack()

        def abririmagem(self, event):
            global filename, fname
            if self.msg["text"] == "Primeira janela":
                self.msg["text"] = "Imagem a ser enviada:"
                self.img = ImageTk.PhotoImage(Image.open(fname))
                self.imagem.pack_forget()
                self.panel = Label(self.master, image = self.img)
                self.panel.pack(side = "bottom", fill = "both", expand = "no")
                self.sair = Button(self.master)

            else:
                self.imagem.pack_forget()
                self.sair = Button(self.master)
                self.sair["text"] = "sair"
                self.sair["font"] = ("Verdana", "15", "bold")
                self.sair["fg"] = ("blue")
                self.sair["width"] = 20
                self.sair.bind("<Button-1>", self.sair.quit())
                self.sair.pack()

        def load_file(self):
            global filename, fname
            opts = {}
            opts['title'] = 'Select file.'
            fname = askopenfilename(**opts)
            #fname = askopenfile(filetypes=[("img files", "*.png;*.jpg;*.jpeg;*.JPG")])
            if fname:
                self.button.pack_forget()
                self.imagem = Button(self.master)
                self.imagem["text"] = "Abrir a imagem"
                self.imagem["font"] = ("Verdana", "15", "bold")
                self.imagem["fg"] = ("blue")
                self.imagem["width"] = 20
                self.imagem.bind("<Button-1>", self.abririmagem)
                self.imagem.pack()

    root = Tk()
    Application(root)
    root.mainloop()

    #Ativa comunicacao

    #filename = askopenfilename()


    com.enable()

    

    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    print ("gerando dados para transmissao :")
    
    if fname != "null":
        with open(fname, "rb") as imageFile:
            imagemenviada = imageFile.read()
            txBuffer = bytearray(imagemenviada)
        txBuffer = bytes(txBuffer)
    else:
        ListTxBuffer =list()
        for x in range(0,100):
            ListTxBuffer.append(x)
        txBuffer = bytes(ListTxBuffer)
    txLen    = len(txBuffer)
    

    tipo = 1
    countP = 1

    # tamanho = 1000

    #HEAD
    #tamanhoEmByte = bytes([txLen])
    while tipo != 7:
        if tipo == 1:
            #print("Tipo (1):             ", tipo)
            txBuffer0 = bytes(1)
            txBuffer0, npacote0 = empacotamento(txBuffer0, txLen, end, stuffing, tipo, 1)
            #print("txBuffer0:             ", txBuffer0)
            while tipo != 2:
                com.sendData(txBuffer0)
                rxBuffer, nRx, erro = com.getData()
                if len(rxBuffer) > 5:
                    tipo = rxBuffer[5]
                if erro:
                    tipo = 1
            #print("rxBuffer:             ", rxBuffer)
            #print("Tipo (2):             ", tipo)
        if tipo == 2:
            tipo = 3
            #print("Tipo (3):             ", tipo)
            txBuffer0 = bytes(1)
            txBuffer0, npacote0 = empacotamento(txBuffer0, txLen, end, stuffing, tipo, 1)
            com.sendData(txBuffer0)
        if tipo == 3:
            tipo = 4
            txBufferD, npacote = empacotamento(txBuffer, txLen, end, stuffing, tipo, countP)
        if tipo == 4:

            #print("Tipo (4):             ", tipo)
            #print("txBuffer:             ", txBuffer)
            time.sleep(0.1)
            com.sendData(txBufferD)
            #time.sleep(2)
            rxBuffer, nRx, erro = com.getData()
            #print("rxBuffer:             ", rxBuffer)
            if len(rxBuffer) > 5:
                tipo = rxBuffer[5]
                countP = rxBuffer[3]
            #print("Tipo (6):             ", tipo)
            if erro:
                tipo = 6
            elif (tipo == 5) and (countP != npacote):
                countP += 1
                tipo = 3
            elif tipo == 5 and countP == npacote:
                tipo = 7
        if tipo == 6:
            print("*************************************************************")
            print("Erro 6")
            print("tentando novamente")
            print("*************************************************************")
            tipo = 3
        elif tipo == 8:
            print("*************************************************************")
            print("Erro 8")
            print("tentando novamente")
            print("*************************************************************")
            tipo = 3

        elif tipo == 9:
            print("*************************************************************")
            print("Erro 9")
            print("tentando novamente")
            print("*************************************************************")
            tipo = 3
            #print("Tipo (1):             ", tipo)

    print("-------------------------")
    print("Enviado corretamente")
    print("-------------------------")
    



    
    # Transmite dado
    # print("tentado transmitir .... {} bytes".format())
    

    
    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()
   

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
