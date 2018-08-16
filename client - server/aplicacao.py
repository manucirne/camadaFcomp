
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
from tkinter import *
from PIL import ImageTk, Image
import os


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
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM3"                  # Windows(variacao de)



print("porta COM aberta com sucesso")



def main():
    # Inicializa enlace ... variavel com possui todos os metodos e propriedades do enlace, que funciona em threading
    com = enlace(serialName)

    # Ativa comunicacao
    com.enable()

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
                return

    root = Tk()
    Application(root)
    root.mainloop()


    # a seguir ha um exemplo de dados sendo carregado para transmissao
    # voce pode criar o seu carregando os dados de uma imagem. Tente descobrir
    #como fazer isso
    print ("gerando dados para transmissao :")
    
    with open("imagem.png", "rb") as imageFile:
        imagemenviada = imageFile.read()
        txBuffer = bytearray(imagemenviada)

    # ListTxBuffer =list()
    # for x in range(0,100):
    #     ListTxBuffer.append(x)
    # txBuffer = bytes(ListTxBuffer)
    txLen    = len(txBuffer)
    print(txLen)

    # Transmite dado
    # print("tentado transmitir .... {} bytes".format())
    com.sendData(txBuffer)
    

    # Encerra comunicação
    print("-------------------------")
    print("Comunicação encerrada")
    print("-------------------------")
    com.disable()

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
