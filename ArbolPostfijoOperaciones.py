from pila import *
import sys
import re

class Nodo:
	def __init__(self , valor):
		self.valor = valor
		self.izquierda = None
		self.derecha = None

class ArbolPosFijo:
        diccionario={}
        
        def buscarOperador(self, caracter):
                if (caracter == '+' or caracter == '-' or caracter == '*'
                        or caracter == '/'):
                        return 1
                elif(type(caracter)==int):
                        return 2
                else:
                        return 0

        def construirDiccionario(self,indice,valor):
            self.diccionario[indice]=[valor]
        def getValorDiccionario(self,indice):
            return self.diccionario.get(indice)


        def evaluar(self, arbol):  
                if arbol.valor=='+':
                    return self.evaluar(arbol.izquierda)+self.evaluar(arbol.derecha)
                if arbol.valor=='-':
                    return self.evaluar(arbol.izquierda)-self.evaluar(arbol.derecha)
                if arbol.valor=='*':
                    return self.evaluar(arbol.izquierda)*self.evaluar(arbol.derecha)
                if arbol.valor=='/':
                    try:
                            return self.evaluar(arbol.izquierda)/self.evaluar(arbol.derecha)
                    except ZeroDivisionError:
                            print("No esta permitida la division entre cero")
                            sys.exit()
                try:
                        return float(arbol.valor)
                except:
                        return (self.getValorDiccionario(arbol.valor))[0]
           
        def evaluarCaracteres(self, aux, l1 , l2):
                errores =0 
                for x in aux:
                        if re.match('^[-+]?[0-9]+$', x):
                                l1.append("val")
                                l2.append(x)
                                #print ("Numero")
                        elif re.match('^[a-z][a-zA-Z_$0-9]*$', x):
                                l1.append("var")
                                l2.append(x)
                                #print ("Letra")
                        elif re.match('[-|=|+|*|/]', x):
                                l1.append("ope")
                                l2.append(x)
                                #print ("Operaciones")
                        else:
                                l1.append("Token No Valido")
                                l2.append(x)
                                errores+=1
                                #print ("Operaciones")
                return errores
                                
                                

        def construirArbol(self, posfijo):
                posfijo.pop()
                variable=posfijo.pop()
                pilaOperador = Pila()
                #Recorra todo el string
                for char in posfijo :

                        # si NO es operador lo apila
                        if self.buscarOperador(char)!=1:
                                arbol = Nodo(char)
                                pilaOperador.apilar(arbol)

                        # Operador
                        else:
                                # desapila dos nodos
                                arbol = Nodo(char)
                                arbol1 = pilaOperador.desapilar()
                                arbol2 = pilaOperador.desapilar()

                                # los convierte en hijos
                                arbol.derecha = arbol1
                                arbol.izquierda = arbol2

                                # Anade nuevo arbol a la pila
                                pilaOperador.apilar(arbol)

                # Al final el ultimo elemento de la pila sera el arbol
                arbol = pilaOperador.desapilar()
                self.construirDiccionario(variable,self.evaluar(arbol))
                return self.evaluar(arbol)
        def imprimirTablaTokens(self,l1 , l2):
                  a = 0
                  for m in l1:
                          print(l1[a] + "   " + l2[a])
                          a = a+1
      

class Main:
        lTipo = []
        lValor = []
        respuesta=1
        err =0
        while(respuesta):
          obj = ArbolPosFijo()
          print("Ingrese los valores del arbol en PosFija separados por un espacio:")
          valorIngresado = input() #Python 2.x raw_input(), 3.x input()
          aux = valorIngresado.split(" ")
          err=obj.evaluarCaracteres(aux, lTipo, lValor)
          if(err==0):
                  
                  print ("El valor resultante es: "+ str(obj.construirArbol(aux)))
          else:
                  obj.imprimirTablaTokens(lTipo,lValor)
                  sys.exit()
                  
          #print("diccionario:"+ str(obj.getValorDiccionario("a")))
          print("Desea continuar? Ingrese 1 para continuar, de lo contrario ingrese 0")
          if(input()=='0'):
                  obj.imprimirTablaTokens(lTipo,lValor)
                  respuesta=0
