from tkinter import * 

#Ventana
my_window = Tk() 
my_window.resizable(0,0) 
my_window.title("coordenadas mouse") 

#funcion
def mostrar_coordenadas(event):
    my_label['text'] = f'x = {event.x} y = {event.y}' 

#creacion lienzo
my_canvas = Canvas(my_window, width=400, height=400, background='gray') 
my_label = Label(bd=4, relief="solid", font="Times 22 bold", bg="white", fg="black") 
my_canvas.bind('<Button-1>', mostrar_coordenadas) 
my_canvas.grid(row=0, column=0) 
my_label.grid(row=1, column=0) 

my_window.mainloop()
