from tkinter import *
from PIL import ImageTk, Image
import os


class Application:
    def __init__(self, master=None):
        self.widget1 = Frame(master)
        self.widget1.pack()
        self.widget1["bg"] = ("lightblue")
        self.msg = Label(self.widget1, text="Primeira janela")
        self.msg["font"] = ("Verdana", "20")
        self.msg["bg"] = ("lightblue")
        self.msg.pack()
        self.imagem = Button(self.widget1)
        self.imagem["text"] = "Ir para a imagem"
        self.imagem["font"] = ("Verdana", "15", "bold")
        self.imagem["fg"] = ("blue")
        self.imagem["width"] = 20
        self.imagem.bind("<Button-1>", self.abririmagem)
        self.imagem.pack()

    def abririmagem(self, event):
        if self.msg["text"] == "Primeira janela":
            self.msg["text"] = "O botão recebeu um clique"
            self.img = ImageTk.PhotoImage(Image.open("img.jpeg"))
            self.panel = Label(self.widget1, image = self.img)
            self.panel.pack(side = "bottom", fill = "both", expand = "yes")
        else:
            self.sair = Button(self.widget1)
            self.sair["text"] = "sair"
            self.sair["font"] = ("Verdana", "15", "bold")
            self.sair["fg"] = ("blue")
            self.sair["width"] = 20
            self.sair.pack()
            self.sair.quit()
root = Tk()
Application(root)
root.mainloop()

# with open("img.jpeg", "rb") as imageFile:
#   f = imageFile.read()
#   b = bytearray(f)

# print (b)