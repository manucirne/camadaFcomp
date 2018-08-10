import tkinter
with open("img.jpeg", "rb") as imageFile:
  f = imageFile.read()
  b = bytearray(f)

print (b)