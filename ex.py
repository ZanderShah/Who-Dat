import Tkinter as tk
from Tkinter import *
import cv2
from PIL import Image, ImageTk

cap = cv2.VideoCapture(0)
root = tk.Tk()
root.bind('<Escape>', lambda e: root.quit())
root.overrideredirect(1)
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
lmain = tk.Label(root, bd="0")

z = Canvas(root, width = root.winfo_screenwidth(), height = root.winfo_screenheight(), borderwidth="0")
z.pack()

def show_frame():
    _, frame = vc.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    img = img.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img)
    imag = z.create_image(0, 0, image=imgtk, anchor='nw')
    lmain.imgtk = imgtk
    test = z.create_text(root.winfo_screenwidth()/2, root.winfo_screenheight() ,text = "Unlock your device with your face!", font=('Comic Sans MS', 50), fill = 'white', anchor = 's', tag = 'test')
    who = Image.open("img/who.jpg")
    who = who.resize((250, 250), Image.ANTIALIAS)
    meme2 = ImageTk.PhotoImage(who)
    whoMeme = Label(z, image=meme2, bd="0")
    whoMeme.image = meme2
    whoMemes = z.create_window(root.winfo_screenwidth(), 0, window=whoMeme, anchor='ne')
    image = Image.open("img/ugly1.jpg")
    image = image.resize((250,250), Image.ANTIALIAS)
    meme1 = ImageTk.PhotoImage(image)
    meme = Label(z, image=meme1, bd="0")
    meme.image = meme1
    memes = z.create_window(0, 0, window=meme, anchor='nw')
    lmain.configure(image=imgtk, bd="0")
    lmain.after(10, show_frame)

lmain.pack()
show_frame()
root.mainloop()
