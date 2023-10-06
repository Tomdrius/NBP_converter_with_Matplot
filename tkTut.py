from tkinter import *
from tkinter import messagebox 

import mysql.connector
import time
from collections import deque

mydb = mysql.connector.connect(host="localhost",user="user",passwd="1234", database="baza")

root = Tk()
root.resizable(width=False, height=True)


def kliknietoPrzycisk():
    print('click')
    print(ent.get())
    t = txt.get('1.0',END)
    t2 = txt.get('1.3','2.0')
    # txt.delete('1.0',END)
    query="SELECT id,regNr FROM cars"
    f = ""
    cursor = mydb.cursor()
    cursor.execute(query)
    for (id,regNr) in cursor:
        f = f + "{} = {}\n".format(id,regNr)
    cursor.close()
    messagebox.showerror("Wpisane dane",ent.get() + t + '\n' + t2)
    txt.insert('2.0',f)


def mouse_move(event):
    print(event.x, event.y)
    c.create_rectagle(event.x+5,event.y+5,event.x-5,event.y-5,outline='pink',fill='blue')

def clear_canvas(event):
    print(c.fing_all())
    deque(map(lambda i: c.delete(i), c.fing_all()))

def on_select(event):
    libox = event.widget
    index = int(libox.curselection()[0])
    print(libox.get(index),index)





haj = Label(root, text="Hello World")
haj.grid(row=0,column=0) #set har in grid

frame = Frame(root,borderwidth=4)
frame.grid(row=0, column=1)
frame.config(background='black')

lab1 = Label(frame,text="Ramka1")
lab1.grid(sticky=W, row=1, column=0, padx=5, pady=5)

przycisk = Button(frame, text='kliknij mnie teraz', command=kliknietoPrzycisk)
przycisk.grid(row=2, column=0)
przycisk.config(background='red', foreground='#FFFF00')

c = Canvas(frame, width=500, height=150)
c.bind('<Button-1>',mouse_move)
c.bind('<Button-3>',clear_canvas)



c.grid(sticky=S, row=3, column=0, padx=5, pady=5)
c.config(background='green')
txt = Text(frame, width=120, height=10)
txt.grid(sticky=E+N, row=4, column=0, padx=5, pady=5)

libox = Listbox(root)
libox.grid(row=4, column=1)
libox.insert(0,'witajcie uczniowie')