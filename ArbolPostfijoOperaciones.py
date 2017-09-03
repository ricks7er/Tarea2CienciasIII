from pila import *
import sys

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




class Main:
        respuesta=1
        while(respuesta):
          obj = ArbolPosFijo()
          print("Ingrese los valores del arbol en PosFija separados por un espacio:")
          valorIngresado = input() #Python 2.x raw_input(), 3.x input()
          aux = valorIngresado.split(" ")
          print ("El valor resultante es: "+ str(obj.construirArbol(aux)))
          print("diccionario:"+ str(obj.getValorDiccionario("a")))
          print("Desea continuar? Ingrese 1 para continuar, de lo contrario ingrese 0")
          if(input()=='0'):
            respuesta=0
