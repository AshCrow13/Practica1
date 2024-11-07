import os
import random
archivo=open('na.txt','w')
Todo = []
lista_aleatorios=[]
 

for i in range(0,5):
  lista = ""
  aux = ""
  for j in range(0,5):
    j=random.randint(0,255)
    lista = lista + str(j)
    archivo.write(str(j)+ ' ') 
  archivo.write(' \n')
  
  lista_aleatorios.append(lista)   
#archivo.write(str(lista_aleatorios)+ '\n')
  
          
        
  
  
  
  
archivo.close()
archivo = open ('na.txt','r')
print(archivo.read())