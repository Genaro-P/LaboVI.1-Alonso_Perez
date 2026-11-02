import numpy as np
import tkinter as tk
from greek_alphabet import Alphabet as alph

#Informatica 2 - 2026
#Integrantes: Alonso Giambelluca Giuliano, Perez Genaro.
#URL del repositorio de Github: https://github.com/Genaro-P/LaboVI.1-Alonso_Perez.git


#Ventana principal

ventana = tk.Tk()
ventana.title("Calculadora de polinomios.")
ventana.geometry("800x750")

tk.Label(ventana, text= "Laboratorio VI.1", relief= "groove", font= ("times new roman", 14)).pack(padx = 5, pady= 1)
tk.Label(ventana, text= "Calculadora para polinomios.", font= ("times new roman", 10)).pack(padx = 5, pady= 1)
tk.Label(ventana, text= "Inserte su polinomio aqui:        (los espacios en blanco se consideraran 0)", font= ("times new roman", 10)).pack(padx = 10, pady= 1, anchor= "w")

#Frame donde se inserta el polinomio
frame_polinomio = tk.Frame(ventana, relief= "flat")
frame_polinomio.pack(padx= 5, pady= 1)
tk.Label(frame_polinomio, text= "Terminos", font= ("times new roman", 8)).grid(row=0, column=0,)
tk.Label(frame_polinomio, text= "Coeficientes", font= ("times new roman", 8)).grid(row=1, column=0,)
label_notdigit = tk.Label(ventana, text= "", font= ("times new roman", 10))
label_notdigit.pack(padx= 10, pady= 1, anchor= "w")

#Funcion para filtrar entradas incorrectas
def digit(event):
    try:
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
tamanio = 10
#Contendra los coeficientes del termino con el exponente que coincida con su indice en la lista

for i in range(tamanio):
    tk.Label(frame_polinomio, text= f"x^{i}" ,font= ("times new roman", 8)).grid(row=0, column= tamanio - i) 
    polinomio.append(tk.Entry(frame_polinomio, font= ("times new roman", 8), relief="sunken", width= 8))
    polinomio[i].grid(row= 1, column= tamanio - i, padx= 4, pady = 2)
    polinomio[i].bind("<KeyRelease>", digit)

def borrar():
    for i in range(tamanio):
        polinomio[i].delete(0,tk.END)
        polinomio[i].insert(0, 0)

def prueba():
    valores_de_prueba = np.array([-25,82,0,-8,0,1])
    for restantes in range(tamanio - 6):
        valores_de_prueba = np.append(valores_de_prueba, 0)
    for i in range(tamanio):
        polinomio[i].delete(0, tk.END)
        polinomio[i].insert(i, valores_de_prueba[i])
    
#Botones para borrar los valores del polinomio y poner los valores de prueba
tk.Button(frame_polinomio, text= "Borrar valores", command= borrar, relief= "groove", font= ("times new roman", 8)).grid(row= 0, column= tamanio + 1, padx= 5)
tk.Button(frame_polinomio, text= "Valores de prueba", command= prueba, relief= "groove", font= ("times new roman", 8)).grid(row= 1, column= tamanio + 1)

#Seccion de calculo de raices
tk.Label(ventana, text= "Calculo de una raiz:", font= ("times new roman", 10)).pack(padx= 12,pady= 1, anchor= "w")
frame_raices = tk.Frame(ventana,  relief= "flat", width= 800, height= 100)
frame_raices.pack(padx= 5, pady= 5)
frame_raices_metodo = tk.Frame(frame_raices, relief= "flat")
frame_raices_metodo.place(relx= 0.05, rely= 0.5, anchor= "w")
frame_raices_calculo = tk.Frame(frame_raices, relief= "flat")
frame_raices_calculo.place(relx= 0.95, rely= 0.5, anchor= "e")
frame_raices_nums = tk.Frame(frame_raices, relief= "flat")
frame_raices_nums.place(relx= 0.5, rely= 0.5, anchor= "center")
label_alerta = tk.Label(ventana, text= "", font= ("times new roman", 10))
label_alerta.pack(padx= 12,pady= 5, anchor= "w")

#Funcion para evaluar el valor del polinomio en cierto x
def evaluar_en(x):
    resultado = 0
    for i in range(tamanio):
        try:
            resultado += float(polinomio[i].get())*(x**i)
        except:
            resultado += 0
    return resultado

#Metodo de biseccion
def biseccion_f(x1, x2):
    if(evaluar_en(x1)*evaluar_en(x2)<=0):
        label_alerta.config(text= "")
        iteraciones = 1
        epsilon_a = 10000 #Valor arbitrariamente grande
        aproximacion_anterior = "x1"
        while(epsilon_a > error_max and iteraciones < maximo):
            if(evaluar_en(x1)==0):
                mitad = x1
                break
            elif(evaluar_en(x2)==0):
                mitad = x2
                break
            else:
                mitad = (x2 + x1)/2
                if(iteraciones > 1):
                    if(aproximacion_anterior == "x1"):
                        epsilon_a = (abs(x1-mitad))/x1
                    else:
                        epsilon_a = (abs(x2-mitad))/x2
                if(evaluar_en(x1)*evaluar_en(mitad)<=0):
                    aproximacion_anterior = "x2"
                    x2 = mitad
                else:
                    aproximacion_anterior = "x1"
                    x1 = mitad
                iteraciones += 1
    else:
        label_alerta.config(text= "El intervalo elegido no es valido, ya que la funcion en ambos extremos tiene el mismo signo.")
        return
    iter_total.config(text= f"{iteraciones}")
    raiz.config(text= f"{mitad:.7f}")
    evaluar_raiz.config(text= f"{evaluar_en(mitad):.5}")
    if(iteraciones > 1):
        epsilon_a_cartel.config(text= f"{(epsilon_a*100):.8f}")
    else:
        epsilon_a_cartel.config(text= "-")
        

#Metodo de Newton - Raphson
def newt_raph_f(x1):
    pendiente = (evaluar_en(x1+0.00001)-evaluar_en(x1-0.00001))/0.00002 #Calcula la derivada con h = 0.00001
    try:
        x2 = x1 - evaluar_en(x1)/pendiente
    except:
        label_alerta.config(text= "El calculo seleccionado diverge.")
        return
    label_alerta.config(text= "")
    iteraciones = 1
    epsilon_a = 10000 
    while(epsilon_a > error_max and iteraciones < maximo):
        x1 = x2
        nueva_pendiente = (evaluar_en(x1+0.0001)-evaluar_en(x1-0.0001))/0.0002
        #Este if() verifica que la pendiente no sea nula o que no tenga el signo 
        #contrario al de la pendiente anterior, por los riesgos a que la aproximacion diverga
        if(abs(nueva_pendiente) > 10**(-15) and pendiente*nueva_pendiente>0): 
            pendiente = nueva_pendiente
            x2 = x1 - evaluar_en(x1)/pendiente
            if(x1 != 0):
                epsilon_a = abs(x1-x2)/x1
            iteraciones += 1
            label_alerta.config(text= "")
        else:
            label_alerta.config(text= "El calculo seleccionado diverge.")
            break
    iter_total.config(text= f"{iteraciones}")
    raiz.config(text= f"{x2:.7f}")
    evaluar_raiz.config(text= f"{evaluar_en(x2):.5}")
    if(iteraciones > 1):
        epsilon_a_cartel.config(text= f"{(epsilon_a*100):.8f}")
    else:
        epsilon_a_cartel.config(text= "-")

#Metodo de la secante
def secante_f(x1, x2):
    pendiente = (evaluar_en(x2)-evaluar_en(x1))/(x2-x1)
    try:
        aproximacion = x1 - evaluar_en(x1)/pendiente
    except:
        label_alerta.config("El calculo seleccionado diverge.")
        return
    label_alerta.config(text= "")
    iteraciones = 1
    epsilon_a = 10000 
    while(epsilon_a > error_max and iteraciones < maximo):
        x1 = x2
        x2 = aproximacion
        nueva_pendiente = (evaluar_en(x2)-evaluar_en(x1))/(x2-x1)
        if(abs(nueva_pendiente) > 10**(-15)): 
            pendiente = nueva_pendiente
            aproximacion = x1 - evaluar_en(x1)/pendiente
            if(x1 != 0):
                epsilon_a = abs(x1-aproximacion)/x1
            iteraciones += 1
            label_alerta.config(text= "")
        else:
            label_alerta.config(text= "El calculo seleccionado diverge.")
            break
    iter_total.config(text= f"{iteraciones}")
    raiz.config(text= f"{aproximacion:.7f}")
    evaluar_raiz.config(text= f"{evaluar_en(aproximacion):.5}")
    if(iteraciones > 1):
        epsilon_a_cartel.config(text= f"{(epsilon_a*100):.8f}")
    else:
        epsilon_a_cartel.config(text= "-")

t_error = "error_s" #Tipo de error por defecto
maximo = 0 #Iteraciones maximas
error_max = 0 #Error dictado por la variable 'epsilon s' o por las cifras significativas

#Funcion para ejecutar el calculo elegido
def calcular():
    global maximo
    global error_max
    try:
        maximo = float(iter_max.get())
    except:
        maximo = 1
    if(t_error == "error_s"):
        try:
            error_max = float(error_s_num.get())/100
        except:
            label_alerta.config(text= "Por favor escribi bien el error considerado.")
            return
    else:
        try:
            error_max = 0.5/(10**(float(cifras_sig_num.get())))
        except:
            label_alerta.config(text= "Por favor escribi bien el error considerado.")
            return
    try:
        x1 = float(xl.get())
    except:
        x1 = 0
    if(metodo == "biseccion"):
        try:
            x2 = float(xu.get())
        except:
            x2 = 0
        if(x1<x2):
            biseccion_f(x1, x2)
        else:
            label_alerta.config(text= "Porfavor ingresa un intervalo tal que xl < xu.")
    if(metodo == "newton - raphson"):
        newt_raph_f(x1)
    if(metodo == "secante"):
        try:
            x2 = float(xu.get())
        except:
            x2 = 0
        if(x1<x2):
            secante_f(x1, x2)
        else:
            label_alerta.config(text= "Porfavor ingresa un intervalo tal que xl < xu.")

metodo = "biseccion" #Metodo elegido por defecto

#Funcion para elegir el metodo
def metodo_raiz(event):
    global metodo
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
biseccion.grid(row=1, column=0, pady=0)
newt_raph = tk.Button(frame_raices_metodo, text= "Newton - Raphson", font= ("times new roman", 8))
newt_raph.bind("<ButtonRelease-1>", metodo_raiz)
newt_raph.grid(row=2, column=0, pady=0)
secante = tk.Button(frame_raices_metodo, text= "Secante", font= ("times new roman", 8))
secante.bind("<ButtonRelease-1>", metodo_raiz)
secante.grid(row=3, column=0, pady=0)

#Seccion del medio, con los valores que se usan para calcular las raices
tk.Label(frame_raices_nums, text= "xl = ", font= ("times new roman", 8)).grid(row= 0, column= 0)
xl = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
xl.grid(row= 0, column= 1, padx= 5)
xl.bind("<KeyRelease>", digit)
tk.Label(frame_raices_nums, text= "xu = ", font= ("times new roman", 8)).grid(row= 0, column= 2)
xu = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
xu.grid(row= 0, column= 3, padx= 5)
xu.bind("<KeyRelease>", digit)
tk.Label(frame_raices_nums, text= "N-R utiliza xl solamente.", font= ("times new roman", 8)).grid(row=0, column=4, padx= 5, columnspan= 3)

#Nada mas para estilizar los botones que eligen el tipo de minimo de error porcentual aproximado
def precision(event):
    global t_error
    error_s.config(background= "white")
    error_s.config(state= "normal")
    cifras_sig.config(background= "white")
    cifras_sig.config(state= "normal")
    event.widget.config(state= "disabled", background = "#d9d9d9")
    if(event.widget == error_s):
        error_s_num.config(state= "normal")
        cifras_sig_num.config(state= "disabled", disabledbackground= "#d9d9d9")
        t_error = "error_s"
    else:
        error_s_num.config(state= "disabled", disabledbackground= "#d9d9d9")
        cifras_sig_num.config(state= "normal")
        t_error = "cifras_sig"

#Botones para elegir el tipo de error porcentual minimo
tk.Label(frame_raices_nums, text= "Selecciona el tipo de precision:", font= ("times new roman", 8)).grid(row= 1, column=0, columnspan=4, pady= 1)
epsilon = alph.Epsilon
error_s = tk.Button(frame_raices_nums, text= f"{epsilon}s (%) = ", font= ("times new roman", 8), state= "disabled", background= "#d9d9d9")
error_s.grid(row= 2, column=0, pady= 0)
error_s.bind("<ButtonRelease-1>", precision)
error_s_num = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
error_s_num.grid(row= 2, column= 1, pady= 0)
error_s_num.bind("<KeyRelease>", digit)
cifras_sig = tk.Button(frame_raices_nums, text= "Cifras significativas = ", font= ("times new roman", 8))
cifras_sig.grid(row= 2, column= 2, columnspan= 2, pady= 0, padx= 5)
cifras_sig.bind("<ButtonRelease-1>", precision)
cifras_sig_num = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8, state= "disabled", disabledbackground= "#d9d9d9")
cifras_sig_num.grid(row= 2, column= 4, pady= 0)
cifras_sig_num.bind("<KeyRelease>", digit)

#Maximas iteraciones
tk.Label(frame_raices_nums, text= "Maximas iteraciones =", font= ("times new roman", 8)).grid(row= 3, column= 1, columnspan= 2, pady= 2)
iter_max = tk.Entry(frame_raices_nums, font= ("times new roman", 8), relief="sunken", width= 8)
iter_max.grid(row= 3, column= 3, pady= 0)
iter_max.bind("<KeyRelease>", digit)

tk.Button(frame_raices_calculo, text= "Calcular", font= ("times new roman", 8), command = calcular).grid(row= 0, column= 0, columnspan= 2, pady= 0)
tk.Label(frame_raices_calculo, text= "Raiz =", font= ("times new roman", 8)).grid(row= 1, column= 0, pady= 0)
raiz = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 12, anchor= "w")
raiz.grid(row= 1, column= 1, pady= 0)
tk.Label(frame_raices_calculo, text= "Iteraciones =", font= ("times new roman", 8)).grid(row= 2, column= 0, pady= 0)
iter_total = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 12, anchor= "w")
iter_total.grid(row= 2, column= 1, pady= 0)
tk.Label(frame_raices_calculo, text= f"{epsilon}a (%) =", font= ("times new roman", 8)).grid(row= 3, column= 0, pady= 0)
epsilon_a_cartel = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 12, anchor= "w")
epsilon_a_cartel.grid(row= 3, column= 1, pady= 0)
tk.Label(frame_raices_calculo, text= f"f(Raiz) =", font= ("times new roman", 8)).grid(row= 4, column= 0, pady= 0)
evaluar_raiz = tk.Label(frame_raices_calculo, font= ("times new roman", 8), relief= "groove", width= 12, anchor= "w")
evaluar_raiz.grid(row= 4, column= 1, pady= 0)



#Seccion de derivada

#Funcion de calculo de derivada por metodo de diferencia centrada
def dif_centrada():
    x_0 = 0
    dx = 0
    try:
        x_0 = float(entrada_x_0.get())
        dx = float(entrada_dx.get())
    except:
        label_alerta.config(text= "Porfavor ingresa los datos necesarios")
        resultado_derivada.config(text= "")
        return
    else:
        label_alerta.config(text= "")
        derivada = (evaluar_en(x_0 + dx)-evaluar_en(x_0 - dx))/(2*dx)
        resultado_derivada.config(text= f"{derivada:.2f}")
        return



tk.Label(ventana, text= "Calculo de la derivada primera con diferencia centrada:", font= ("times new roman", 10)).pack(padx= 5, pady= 2, anchor= "w")
frame_derivada = tk.Frame(ventana, relief= "flat")
frame_derivada.pack(padx= 5, pady= 2)
tk.Label(frame_derivada, text= "x0 =", font= ("times new roman", 8)).pack(padx= 5, pady= 0, side= "left")
entrada_x_0 = tk.Entry(frame_derivada, font= ("times new roman", 8), relief= "sunken", width= 8)
entrada_x_0.pack(padx= 5, pady= 0, side= "left")
entrada_x_0.bind("<KeyRelease>", digit)
tk.Label(frame_derivada, text= "dx =", font= ("times new roman", 8)).pack(padx= 5, pady= 0, side= "left")
entrada_dx = tk.Entry(frame_derivada, font= ("times new roman", 8), relief= "sunken", width= 8)
entrada_dx.pack(padx= 5, pady= 0, side= "left")
entrada_dx.bind("<KeyRelease>", digit)
#Boton de calculo
tk.Button(frame_derivada, text= "Calcular", font= ("times new roman", 8), command= dif_centrada).pack(padx= 5, pady= 0, side= "left")
tk.Label(frame_derivada, text= "f '(x0) =", font= ("times new roman", 9)).pack(padx= 5, pady= 0, side= "left")
resultado_derivada = tk.Label(frame_derivada, font= ("times new roman", 8), relief= "groove", width= 20)
resultado_derivada.pack(padx= 5, pady= 0, side= "left")




#Seccion de sistemas de ecuaciones lineales

#Metodo de gauss con o sin pivoteo parcial
def gauss(A, B, pivoteo=False):
    A = np.array(A, dtype=float).copy()
    B = np.array(B, dtype=float).copy()

    n = len(B)

    # Eliminacion hacia adelante
    for k in range(n):

        # Pivoteo parcial
        if pivoteo:
            fila_max = k + np.argmax(np.abs(A[k:, k]))

            A[[k, fila_max]] = A[[fila_max, k]]
            B[[k, fila_max]] = B[[fila_max, k]]

        # Verificacion del pivote
        if abs(A[k, k]) < 1e-12:
            raise ValueError(
                f"Pivote nulo en la columna {k + 1}."
            )

        # Anulacion de los elementos debajo del pivote
        for i in range(k + 1, n):

            factor = A[i, k] / A[k, k]

            A[i, k:] -= factor * A[k, k:]
            B[i] -= factor * B[k]

    # Sustitucion regresiva
    X = np.zeros(n)

    for i in range(n - 1, -1, -1):

        suma = 0

        for j in range(i + 1, n):
            suma += A[i, j] * X[j]

        X[i] = (B[i] - suma) / A[i, i]

    return X


tk.Label(
    ventana,
    text="Sistemas de ecuaciones lineales:",
    font=("times new roman", 10)
).pack(padx=12, pady=2, anchor="w")

frame_sistema = tk.Frame(
    ventana,
    relief= "flat"
)
frame_sistema.pack(padx=5, pady=2)

# Matriz de entradas
entradas_sistema = []

tk.Label(
    frame_sistema,
    text="Coeficientes",
    font=("times new roman", 8)
).grid(row=0, column=0, columnspan=4)

tk.Label(
    frame_sistema,
    text="Termino independiente",
    font=("times new roman", 8)
).grid(row=0, column=4)

for i in range(4):

    fila = []

    for j in range(5):

        entrada = tk.Entry(
            frame_sistema,
            font=("times new roman", 8),
            width=7
        )
        entrada.grid(
            row=i+1,
            column=j,
            padx=4,
            pady=0
        )
        entrada.bind("<KeyRelease>", digit)

        fila.append(entrada)

    entradas_sistema.append(fila)


# Funcion para cargar los valores de prueba
def prueba_sistema():

    valores = [
        [2, 2, 1, -1, 5],
        [2, -2, 6, -4, 0],
        [2, 2, 1, 1, 13],
        [1, 5, -4, -2, -9]
    ]

    for i in range(4):
        for j in range(5):

            entradas_sistema[i][j].delete(0, tk.END)

            entradas_sistema[i][j].insert(
                0, str(valores[i][j])
            )


# Funcion para borrar los campos
def borrar_sistema():

    for i in range(4):
        for j in range(5):

            entradas_sistema[i][j].delete(0, tk.END)


# Funcion para obtener los datos y ejecutar Gauss
def calcular_sistema(pivoteo):

    try:

        A = []
        B = []

        for i in range(4):

            fila = []

            for j in range(4):

                valor = entradas_sistema[i][j].get()

                if valor.strip() == "":
                    raise ValueError("Hay campos vacios.")

                fila.append(float(valor))

            termino = entradas_sistema[i][4].get()

            if termino.strip() == "":
                raise ValueError("Hay campos vacios.")

            A.append(fila)
            B.append(float(termino))

        resultado = gauss(A, B, pivoteo)

        for i in range(4):

            resultados_sistema[i].config(
                text=f"{resultado[i]:.8g}",
                fg="black"
            )
        label_alerta_sistema.config(text="")
         
    
    except ValueError as error:

        for label in resultados_sistema:
            label.config(text="", fg="red")

        label_alerta_sistema.config(
            text=f"Error: {error}",
            fg="red"
        )


# Botones
tk.Button(
    frame_sistema,
    text="Valores de prueba",
    command=prueba_sistema,
    font=("times new roman", 8)
).grid(row=5, column=0, columnspan=2, pady=2)

tk.Button(
    frame_sistema,
    text="Borrar",
    command=borrar_sistema,
    font=("times new roman", 8)
).grid(row=5, column=2, pady=2)

tk.Button(
    frame_sistema,
    text="Gauss sin pivoteo",
    command=lambda: calcular_sistema(False),
    font=("times new roman", 8)
).grid(row=5, column=3, pady=2)

tk.Button(
    frame_sistema,
    text="Gauss con pivoteo",
    command=lambda: calcular_sistema(True),
    font=("times new roman", 8)
).grid(row=5, column=4, pady=2)



# Frame para mostrar los resultados
frame_resultado_sistema = tk.Frame(
    ventana,
    relief= "flat"
)

frame_resultado_sistema.pack(padx=5, pady=2)

# Labels para cada incognita
tk.Label(
    frame_resultado_sistema,
    text="Resultados:",
    font=("times new roman", 9)
).grid(row=0, column=0, columnspan=4, pady=1)

resultados_sistema = []

for i in range(4):

    tk.Label(
        frame_resultado_sistema,
        text=f"x{i+1} = ",
        font=("times new roman", 9)
    ).grid(row=1, column=2*i, padx=3, pady=1)

    label = tk.Label(
        frame_resultado_sistema,
        text="",
        font=("times new roman", 9),
        relief="groove",
        width=10
    )

    label.grid(row=1, column=2*i+1, padx=3, pady=1)

    resultados_sistema.append(label)

label_alerta_sistema = tk.Label(
    ventana,
    text="",
    font=("times new roman", 9)
)

label_alerta_sistema.pack(padx=12, pady=1, anchor="w")

#Seccion de integrales

# Metodo de Simpson 1/3 compuesto
def simpson_compuesta(a, b, n):

    if n < 2 or n % 2 != 0:
        raise ValueError("La cantidad de segmentos debe ser par y mayor o igual a 2.")

    h = (b - a) / n

    # Se evaluan los extremos del intervalo
    resultado = evaluar_en(a) + evaluar_en(b)

    # Se suman los puntos interiores
    suma_impares = 0
    suma_pares = 0

    for i in range(1, n):
        x = a + i * h

        if i % 2 != 0:
            suma_impares += evaluar_en(x)
        else:
            suma_pares += evaluar_en(x)

    resultado += 4 * suma_impares
    resultado += 2 * suma_pares

    return (h / 3) * resultado

tk.Label(ventana, text="Calculo de una integral:",font=("times new roman", 10)).pack(padx=12, pady=5, anchor="w")

frame_integral = tk.Frame(
    ventana, relief= "flat")
frame_integral.pack(padx=5, pady=5)

# Entradas para los parametros
frame_integral_nums = tk.Frame(frame_integral)
frame_integral_nums.pack(side="left", padx=15, pady=10)

tk.Label(frame_integral_nums, text="Limite inferior (a):",font=("times new roman", 8)).grid(row=0, column=0)

a_integral = tk.Entry(frame_integral_nums, font=("times new roman", 8), width=8)
a_integral.grid(row=0, column=1, padx=5)
a_integral.insert(0, "0")
a_integral.bind("<KeyRelease>", digit)

tk.Label(frame_integral_nums, text="Limite superior (b):",font=("times new roman", 8)).grid(row=1, column=0)

b_integral = tk.Entry(frame_integral_nums, font=("times new roman", 8), width=8)
b_integral.grid(row=1, column=1, padx=5)
b_integral.insert(0, "2")
b_integral.bind("<KeyRelease>", digit)

tk.Label(frame_integral_nums, text="Segmentos (n):",font=("times new roman", 8)).grid(row=2, column=0)

n_integral = tk.Entry(frame_integral_nums, font=("times new roman", 8), width=8)
n_integral.grid(row=2, column=1, padx=5)
n_integral.insert(0, "2")
n_integral.bind("<KeyRelease>", digit)


# Funcion para ejecutar el calculo
def calcular_integral():
    try:
		# Verificar que ningun campo este vacio
        if (a_integral.get().strip() == "" or
            b_integral.get().strip() == "" or
            n_integral.get().strip() == ""):

            raise ValueError("Completa todos los campos.")
        
        a = float(a_integral.get())
        b = float(b_integral.get())
        n = int(n_integral.get())

        if not np.isfinite(a) or not np.isfinite(b):
            raise ValueError("Los limites deben ser valores finitos.")

        if n < 2 or n % 2 != 0:
            raise ValueError("n debe ser par y mayor o igual a 2.")

        resultado = simpson_compuesta(a, b, n)

        if not np.isfinite(resultado):
            raise ValueError("El resultado no es finito.")

        label_resultado_integral.config(
            text=f"{resultado:.8g}", fg="black")

        label_alerta_integral.config(text="")

    except ValueError as error:
        label_resultado_integral.config(text="")
        label_alerta_integral.config(
            text=f"Error: {error}", fg="red")


# Boton de calculo
tk.Button(frame_integral, text="Calcular",
          font=("times new roman", 8),
          command=calcular_integral).pack(
              side="left", padx=15, pady=10)


# Resultados
frame_integral_resultado = tk.Frame(frame_integral)
frame_integral_resultado.pack(side="left", padx=15, pady=10)

tk.Label(frame_integral_resultado, text="Integral aproximada:",
         font=("times new roman", 8)).pack()

label_resultado_integral = tk.Label(
    frame_integral_resultado,
    font=("times new roman", 10),
    relief="groove",
    width=12)

label_resultado_integral.pack(pady=3)

label_alerta_integral = tk.Label(
    ventana, text="", font=("times new roman", 9), fg="red")

label_alerta_integral.pack(padx=12, pady=3, anchor="w")


ventana.mainloop()