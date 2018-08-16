from tkinter import *
from PIL import ImageTk, Image
import os


from tkinter.filedialog import askopenfilename, askopenfile
from tkinter.messagebox import showerror

fname = "null"

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
            self.msg["text"] = "Imagem recebida:"
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

# with open("img.jpeg", "rb") as imageFile:
#   f = imageFile.read()
#   b = bytearray(f)

# print (b)