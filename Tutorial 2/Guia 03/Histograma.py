#Este código lee un archivo de texto llamado "na.txt" para mostrar un histograma. 

def limpiar_array_float(lista):
      return [x for x in lista if x != ""]
#La primera opción es para mostrar el histograma, en la segunda se muestra el contenido del txt y en la tercera se sale del programa.
try:
    #Imprime los enunciados de las opciones que se tienen
    print("Histograma")
    print("\n")
    print("1. Mostrar histograma")
    print("2. contenido txt")
    print("3. Salir")
    #Se lee la opción elegida
    opcion = int(input("Ingrese numero de opcion: "))
    #Si se elige la primera opcioón
    if (opcion == 1):
        #Se abre el archivo
        fichero = open('na.txt','r')
        #Se lee el archivo
        arr = fichero.read()
        #Se remplaza los saltos de linea por nada
        data = arr.replace("\n", "" )
        #Se separa los datos por espacio
        data_replace = data.split(" ")
        #Se limpia el array de datos
        mostrar = limpiar_array_float(data_replace)
        #Se crea un diccionario para guardar los datos
        frecuencias = {}
        #Ciclo para guardar los datos en el diccionario
        for i in range(len(mostrar)):
                numero = mostrar[i]
                if numero not in frecuencias:
                    frecuencias[numero] = 1
                else:
                    frecuencias[numero] += 1
        #Ciclo para ordenar e imprimir los datos
        for numero, frecuencia in sorted(frecuencias.items(), key=lambda x: x[1], reverse=True):
            print(numero, "\t", frecuencia*"#")
  
            
        fichero.close

    #Si se elige la segunda opción
    elif (opcion == 2):
        #Se abre el archivo
        Leer = open('na.txt','r')
        #Se imprime el contenido 
        print(Leer.read())
#En caso de que se ingrese una opción que no está entre las disponibles
except:
    print("Has salido")