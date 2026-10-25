import numpy as np
import tkinter as tk

#Informatica 2 - 2026
#Integrantes: Alonso Giambelluca Giuliano, Perez Genaro.
#URL del repositorio de Github: https://github.com/Genaro-P/LaboVI.1-Alonso_Perez.git


#Estoy obsesionado con la idea de utilizar polinomios 
#mas grandes del que nos piden, pero por ahora no.

#Ventana principal

ventana = tk.Tk()
ventana.title("Calculadora de polinomios.")
ventana.geometry("800x700")

tk.Label(ventana, text= "Laboratorio VI.1", relief= "groove", font= ("times new roman", 18)).pack(padx = 5, pady= 5)
tk.Label(ventana, text= "Calculadora para polinomios.", font= ("times new roman", 12)).pack(padx = 5, pady= 5)
tk.Label(ventana, text= "Inserte su polinomio aqui:", font= ("times new roman", 11)).pack(padx = 10, pady= 5, anchor= "w")

#Frame donde se inserta el polinomio
frame_polinomio = tk.Frame(ventana, relief= "solid", borderwidth= 2)
frame_polinomio.pack(padx= 5, pady= 5)
tk.Label(frame_polinomio, text= "Terminos", font= ("times new roman", 11)).grid(row=0, column=0,)
tk.Label(frame_polinomio, text= "Coeficientes", font= ("times new roman", 11)).grid(row=1, column=0,)
label_notdigit = tk.Label(ventana, text= "", font= ("times new roman", 11))
label_notdigit.pack(padx= 10, pady= 5, anchor= "w")

def digit(event):
    try:
        #Ahora filtra cualquier tecla que no es un digito, 
        #simbolo negativo, decimal, las felchas horizontales y el boton de borrar
        if ((48 > event.keycode) or (57 < event.keycode) and event.keycode != 190 and event.keycode != 189):
            if (event.keysym != ("Left") and event.keysym != ("Right") and event.keysym != ("BackSpace")):
                raise ValueError
    except ValueError:
        #Saltea el caso de entrada vacia
        if(event.widget.get().strip() != ""):
            label_notdigit.config(text= "Por favor, solo ingresa digitos o los \n simbolos correctos.")
        #Borra cualquier contenido de la entrada
        event.widget.delete(0, tk.END)
    else:
        label_notdigit.config(text= "")
    print(event.keycode)

polinomio = [] 
tamanio = 8
#Contendra los coeficientes del termino con el exponente que coincida con su indice en la lista, muy util

for i in range(tamanio):
    tk.Label(frame_polinomio, text= f"x^{i}" ,font= ("times new roman", 11)
             ).grid(row=0, column= tamanio-i)
    polinomio.append(tk.Entry(frame_polinomio, font= ("times new roman", 11), relief="sunken", width= 8))
    polinomio[i].grid(row= 1, column= i+1, padx= 4, pady = 8)
    polinomio[i].bind("<KeyRelease>", digit)

def borrar():
    for i in range(tamanio):
        polinomio[i].delete(0,tk.END)
        polinomio[i].insert(0, 0)

def prueba():
    valores_de_prueba = np.array([1,0,-8,0,82,-25])
    for restantes in range(tamanio - 6):
        valores_de_prueba = np.insert(valores_de_prueba, 0,0)
    for i in range(tamanio):
        polinomio[i].delete(0, tk.END)
        polinomio[i].insert(0, valores_de_prueba[i])
    

tk.Button(frame_polinomio, text= "Borrar valores", command= borrar, relief= "groove", font= ("times new roman", 11)
          ).grid(row= 0, column=tamanio+1, padx=5)
tk.Button(frame_polinomio, text= "Valores de prueba", command= prueba, relief= "groove", font= ("times new roman", 11)
          ).grid(row= 1, column=tamanio + 1)
                          



ventana.mainloop()
