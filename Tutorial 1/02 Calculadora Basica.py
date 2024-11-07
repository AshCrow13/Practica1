#Titulo
print("calculadora") 
print("Ingrese las variables a sumar, restar y multiplicar")
#primer numero  de la calculadora
print("\n Ingrese el primer numero:")
a = int(input())
#Segundo numero de la calculadora
print("Ingrese el segundo numero")
#Guardaremos el nuevo numero 
b = int(input())
#Sumaremos ambos numeros 
s = a + b 
#Mostraremos el resultado por pantalla
print(f"valor de la suma es: {s}")
#la resta
r = a - b 
#Muestra la  resta
print(f"valor de la resta es: {r}")
#La multiplicacion 
m = a * b 
#Mostramos la multiplicacion 
print(f"valorde la multiplicacion es: {m}")

print("\n Ingrese el primer valor a dividir")
x = int(input())
print("ingrese el segundo valor distinto a 0")
y = int(input()) 

d = x / y
print(f"valor de la division es: {d}")
