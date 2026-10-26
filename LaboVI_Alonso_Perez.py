from re import A
import numpy as np
import tkinter as tk
from greek_alphabet import Alphabet as alph

#Informatica 2 - 2026
#Integrantes: Alonso Giambelluca Giuliano, Perez Genaro.
#URL del repositorio de Github: https://github.com/Genaro-P/LaboVI.1-Alonso_Perez.git


#Estoy obsesionado con la idea de utilizar polinomios 
#mas grandes del que nos piden, pero por ahora no.

#Ventana principal

ventana = tk.Tk()
ventana.title("Calculadora de polinomios.")
ventana.geometry("800x700")

tk.Label(ventana, text= "Laboratorio VI.1", relief= "groove", font= ("times new roman", 14)).pack(padx = 5, pady= 5)
tk.Label(ventana, text= "Calculadora para polinomios.", font= ("times new roman", 10)).pack(padx = 5, pady= 5)
tk.Label(ventana, text= "Inserte su polinomio aqui:        (los espacios en blanco se consideraran 0)", font= ("times new roman", 10)).pack(padx = 10, pady= 5, anchor= "w")

#Frame donde se inserta el polinomio
frame_polinomio = tk.Frame(ventana, relief= "solid", borderwidth= 2)
frame_polinomio.pack(padx= 5, pady= 5)
tk.Label(frame_polinomio, text= "Terminos", font= ("times new roman", 8)).grid(row=0, column=0,)
tk.Label(frame_polinomio, text= "Coeficientes", font= ("times new roman", 8)).grid(row=1, column=0,)
label_notdigit = tk.Label(ventana, text= "", font= ("times new roman", 10))
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
            label_notdigit.config(text= "Por favor, solo ingresa digitos o los simbolos correctos. (Usamos '.' para decimales).")
        event.widget.delete(0, tk.END)
        #Borra cualquier contenido de la entrada
    else:
        label_notdigit.config(text= "")

polinomio = [] 
tamanio = 8
#Contendra los coeficientes del termino con el exponente que coincida con su indice en la lista, muy util

for i in range(tamanio):
    tk.Label(frame_polinomio, text= f"x^{i}" ,font= ("times new roman", 8)
             ).grid(row=0, column= tamanio - i) 
    polinomio.append(tk.Entry(frame_polinomio, font= ("times new roman", 8), relief="sunken", width= 8))
    polinomio[i].grid(row= 1, column= tamanio - i, padx= 4, pady = 8)
    #La lista de las entradas para los coeficientes esta hecha en orden CRECIENTE, el primer
    #elemento corresponde al coeficiente del termino x^0, el segundo elemento es el de x^1, y asi
    polinomio[i].bind("<KeyRelease>", digit)

def borrar():
    for i in range(tamanio):
        polinomio[i].delete(0,tk.END)
        polinomio[i].insert(0, 0)

def prueba():
    valores_de_prueba = np.array([-25,82,0,8,0,1])
    for restantes in range(tamanio - 6):
        valores_de_prueba = np.append(valores_de_prueba, 0)
    for i in range(tamanio):
        polinomio[i].delete(0, tk.END)
        polinomio[i].insert(i, valores_de_prueba[i])
    
#Botones para borrar los valores del polinomio y poner los valores de prueba
tk.Button(frame_polinomio, text= "Borrar valores", command= borrar, relief= "groove", font= ("times new roman", 8)
          ).grid(row= 0, column= tamanio + 1, padx= 5)
tk.Button(frame_polinomio, text= "Valores de prueba", command= prueba, relief= "groove", font= ("times new roman", 8)
          ).grid(row= 1, column= tamanio + 1)

#Seccion de calculo de raices
tk.Label(ventana, text= "Calculo de una raiz:", font= ("times new roman", 10)).pack(padx= 12,pady= 5, anchor= "w")
frame_raices = tk.Frame(ventana, borderwidth= 2, relief= "solid", width= 800, height= 140)
frame_raices.pack(padx= 5, pady= 5)
frame_raices_metodo = tk.Frame(frame_raices, borderwidth= 2, relief= "solid")
frame_raices_metodo.place(relx= 0.05, rely= 0.5, anchor= "w")
frame_raices_calculo = tk.Frame(frame_raices, borderwidth= 2, relief = "solid")
frame_raices_calculo.place(relx= 0.95, rely= 0.5, anchor= "e")
frame_raices_nums = tk.Frame(frame_raices, borderwidth= 2, relief= "solid")
frame_raices_nums.place(relx= 0.5, rely= 0.5, anchor= "center")
label_alerta = tk.Label(ventana, text= "", font= ("times new roman", 10))
label_alerta.pack(padx= 12,pady= 5, anchor= "w")

#Funcion para evaluar el valor del polinomio en cierto x
def evaluar_en(x):
    resultado = 0
    for i in range(tamanio):
        resultado += float(polinomio[i].get())*(x^i)
    return resultado

#Metodo de biseccion
def biseccion(x1, x2, iteraciones):
    if(evaluar_en(x1)*evaluar_en(x2) <= 0):
        if(evaluar_en(x1) == 0):
            raiz.config(text= f"{x1}")
            iter_total.config(text= f"{iteraciones}")
            error_a.config(text= "0")
            evaluar_raiz.config(text= "0")
        elif(evaluar_en(x2) == 0):
            raiz.config(text= f"{x2}")
            iter_total.config(text= f"{iteraciones}")
            error_a.config(text= "0")
            evaluar_raiz.config(text= "0")
        else: 
            algo = 3
    else:
        if(iteraciones == 0):
            #Se ingreso un intervalo invalido donde no se puede 
            #verificar los requisitos para el uso de la biseccion
            label_alerta.config(text= "El intervalo (xl, xu) ingresado es invalido, el producto no da negativo.")
            raiz.config(text= "")
            iter_total.config(text= "")
            error_a.config(text= "")
            evaluar_raiz.config(text= "")


#Funcion para ejecutar el calculo elegido
def calcular():
    if(metodo == "biseccion"):
        '''try:
            if()'''
        biseccion(float(xl.get()), float(xu.get()), 0)
    if(metodo == "newton - raphson"):
        algo = 1
    if(metodo == "secante"):
        algo = 2

metodo = "biseccion" #Metodo elegido por defecto

#Funcion para elegir el metodo
def metodo_raiz(event):
    biseccion.config(background= "white")
    biseccion.config(state= "normal")
    newt_raph.config(background= "white")
    newt_raph.config(state= "normal")
    secante.config(background= "white")
    secante.config(state= "normal")
    event.widget.config(state= "disabled", background= "#d9d9d9")
    if(event.widget == biseccion):
        metodo = "biseccion"
    elif(event.widget == newt_raph):
        metodo = "newton - raphson"
    elif(event.widget == secante):
        metodo = "secante"



#Botones para cada metodo
tk.Label(frame_raices_metodo, text= "Metodo:", font= ("times new roman", 8)).grid(row=0, column=0)
biseccion = tk.Button(frame_raices_metodo, text= "Biseccion", font= ("times new roman", 8), state= "disabled", background= "#d9d9d9")
biseccion.bind("<ButtonRelease-1>", metodo_raiz)
biseccion.grid(row=1, column=0, pady=2)
newt_raph = tk.Button(frame_raices_metodo, text= "Newton - Raphson", font= ("times new roman", 8))
newt_raph.bind("<ButtonRelease-1>", metodo_raiz)
newt_raph.grid(row=2, column=0, pady=2)
secante = tk.Button(frame_raices_metodo, text= "Secante", font= ("times new roman", 8))
secante.bind("<ButtonRelease-1>", metodo_raiz)
secante.grid(row=3, column=0, pady=2)

#Seccion del medio, con los valores que se usan para calcular las raices
tk.Label(frame_raices_nums, text= "xl = ", font= ("times new roman", 8)).grid(row= 0, column= 0)
xl = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
xl.grid(row= 0, column= 1, padx= 5)
xl.bind("<KeyRelease>", digit)
tk.Label(frame_raices_nums, text= "xu = ", font= ("times new roman", 8)).grid(row= 0, column= 2)
xu = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
xu.grid(row= 0, column= 3, padx= 5)
xu.bind("<KeyRelease>", digit)

#Nada mas para estilizar los botones que eligen el tipo de minimo de error porcentual aproximado
def precision(event):
    error_s.config(background= "white")
    error_s.config(state= "normal")
    cifras_sig.config(background= "white")
    cifras_sig.config(state= "normal")
    event.widget.config(state= "disabled", background = "#d9d9d9")
    if(event.widget == error_s):
        error_s_num.config(state= "normal")
        cifras_sig_num.config(state= "disabled", disabledbackground= "#d9d9d9")
    else:
        error_s_num.config(state= "disabled", disabledbackground= "#d9d9d9")
        cifras_sig_num.config(state= "normal")

#Botones para elegir el tipo de error porcentual minimo
tk.Label(frame_raices_nums, text= "Selecciona el tipo de precision:", font= ("times new roman", 8)
         ).grid(row= 1, column=0, columnspan=4, pady= 2)
epsilon = alph.Epsilon
error_s = tk.Button(frame_raices_nums, text= f"{epsilon}s (%) = ", font= ("times new roman", 8), state= "disabled", background= "#d9d9d9")
error_s.grid(row= 2, column=0, pady= 2)
error_s.bind("<ButtonRelease-1>", precision)
error_s_num = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
error_s_num.grid(row= 2, column= 1, pady= 2)
error_s_num.bind("<KeyRelease>", digit)
cifras_sig = tk.Button(frame_raices_nums, text= "Cifras significativas = ", font= ("times new roman", 8))
cifras_sig.grid(row= 2, column= 2, columnspan= 2, pady= 2, padx= 5)
cifras_sig.bind("<ButtonRelease-1>", precision)
cifras_sig_num = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8, state= "disabled", disabledbackground= "#d9d9d9")
cifras_sig_num.grid(row= 2, column= 4, pady= 2)
cifras_sig_num.bind("<KeyRelease>", digit)

#Maximas iteraciones
tk.Label(frame_raices_nums, text= "Maximas iteraciones =", font= ("times new roman", 8)
         ).grid(row= 3, column= 1, columnspan= 2, pady= 2)
iter_max = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
iter_max.grid(row= 3, column= 3, pady= 2)
iter_max.bind("<KeyRelease>", digit)

tk.Button(frame_raices_calculo, text= "Calcular", font= ("times new roman", 8), command = calcular
          ).grid(row= 0, column= 0, columnspan= 2, pady= 2)
tk.Label(frame_raices_calculo, text= "Raiz =", font= ("times new roman", 8)
         ).grid(row= 1, column= 0, pady= 2)
raiz = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 8)
raiz.grid(row= 1, column= 1, pady= 2)
tk.Label(frame_raices_calculo, text= "Iteraciones =", font= ("times new roman", 8)
         ).grid(row= 2, column= 0, pady= 2)
iter_total = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 8)
iter_total.grid(row= 2, column= 1, pady= 2)
tk.Label(frame_raices_calculo, text= f"{epsilon}a (%) =", font= ("times new roman", 8)
         ).grid(row= 3, column= 0, pady= 2)
error_a = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 8)
error_a.grid(row= 3, column= 1, pady= 2)
tk.Label(frame_raices_calculo, text= f"f(Raiz) =", font= ("times new roman", 8)
         ).grid(row= 4, column= 0, pady= 2)
evaluar_raiz = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 8)
evaluar_raiz.grid(row= 4, column= 1, pady= 2)




ventana.mainloop()