from pila import *
import sys
import re
import ply.lex as lex

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

        def analisis_lex(self,caracteres):
                tokens = [ 'variable','entero','mas','menos','multiplicacion','division', 'igual' ]
                t_ignore = ' \t\n'
                t_mas = r'\+'
                t_menos = r'-'
                t_multiplicacion = r'\*'
                t_division = r'/'
                t_igual = r'='
                #t_variable = r'[a-zA-Z_$0-9]+$'
                t_variable = r'[a-z][a-zA-Z0-9_]*'
                def t_entero(t):
                        r'\d+'
                        t.value = int(t.value)
                        return t
                def t_error(t):
                        print("Caracteres ilegales '%s'" % t.value[0])
                        t.lexer.skip(1)
                lex.lex()
                lex.input(caracteres)
                while True:
                        tok = lex.token()
                        if not tok: break
                        print(str(tok.value) + " - " + str(tok.type))

                
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
          #print("Ingrese los valores del arbol en PosFija separados por un espacio:")
          #valorIngresado = input() #Python 2.x raw_input(), 3.x input()
          filename = sys.argv[1]
          file = open(filename)
          characters = file.read()
          aux = characters.split(" ")
          file.close()
          obj.analisis_lex(characters)
                           
          #err=obj.evaluarCaracteres(aux, lTipo, lValor)
##          if(err==0):
##                  
##                  print ("El valor resultante es: "+ str(obj.construirArbol(aux)))
##          else:
##                  obj.imprimirTablaTokens(lTipo,lValor)
##                  sys.exit()
##                  
          #print("diccionario:"+ str(obj.getValorDiccionario("a")))
          print("Desea continuar? Ingrese 1 para continuar, de lo contrario ingrese 0")
          if(input()=='0'):
                  obj.imprimirTablaTokens(lTipo,lValor)
                  respuesta=0
