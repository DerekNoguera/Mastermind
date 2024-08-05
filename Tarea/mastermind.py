#                                                Mastermind
import random 
import time
from colored import fg, attr
red = fg('red')
green = fg('green')
blue = fg('blue')
magenta = fg('magenta')
reset = attr('reset')
colores = ['red','blue','green','yellow', 'white', 'black',]  #lista de colores

def Escoger_Jugador():
    eleccion = input("\nElige 1 para ser el creador \nElige 2 para ser el adivinador \nEscribe 'Exit' para salir:\n")
    return eleccion

class Computadora:
    def __init__(self, lista_colores):
        self.__lista_colores = lista_colores  #recibe la lista de colores
    
    @property
    def lista_colores(self):
        return self.__lista_colores

class Jugador:
    def __init__(self, lista_colores):  
        self.__lista_colores = lista_colores #tambien recibe la lista de colores
        self.__comando_lista = []
    @property
    def lista_colores(self):
        return self.__lista_colores
    
    @property
    def comando_lista(self):
        return self.__comando_lista
    
    def crear_codigo(self): # si jugador elige ser creador entonces crea un codigo con 4 optiones de colores
        
        print('Crea tu código eligiendo 4 colores de la lista:', ' '.join(self.__lista_colores)) # en el input pone los colores separados por coma, pasa por un strip() para eliminar los espacios# y se usa split() para separarlos por ','
        codigo = input('Ingresa los colores separados por comas (ejemplo: red,blue,green,yellow): ').lower()
        return [color.strip() for color in codigo.split(',')]
    
    def adivinar(self, codigo_de_juego, __intentos, __restante_intentos, tablero): #recibe esos datos de la class Game #lo mismo de crear el codigo pero aqui escrube para adivinarlo y no para crearlo, pasa por los mismos metodos
        print(f'\nAdivina el código \nOpciones {self.__lista_colores}\n')
        codigo_adivinar = input('Ingresa los colores separados por comas (ejemplo: red,blue,green,yellow):').lower()
        
        if codigo_adivinar == '/list':
            if self.comando_lista == []:
                print(f'\n{red}No hay registro disponible{reset}\n')   
            else:
                print(f'\n{green}- {reset}Tus ultimas jugadas fueron')
                for i, jugadas in enumerate(self.comando_lista, 1):
                    print(f' {green}{i} {reset}{jugadas}')    
            return 'list'
                                    
        else:
            codigo_adivinar_arreglado = [color.strip() for color in codigo_adivinar.split(',')]
            self.__comando_lista.append(codigo_adivinar_arreglado)
            tablero.actualizar_tablero(codigo_adivinar_arreglado)
            
            if codigo_adivinar_arreglado == codigo_de_juego:
                
                print(f'\n{green}¡Felicidades! Adivinaste el código en {__intentos} intentos.{reset}')
                tablero.mostrar_tablero()
                
                print(f'La combinacion de colores era {codigo_de_juego}')
                return True
            
            else:
                print(f'\n {red}{__intentos + 1} {reset}Intento incorrecto. \n{green}{__restante_intentos - 1}{reset} intentos restantes\n')
                print(f'Tu ultimo movimiento fue {green}{codigo_adivinar_arreglado}{reset}\n')
                return False
    
            
class Tablero:
    def __init__(self, codigo_de_juego, jugador, filas=12, columnas=4):
        self.__filas = filas   
        self.__columnas = columnas 
        self.__codigo_de_juego = codigo_de_juego
        self.__tablero = self.crear_tablero() 
        self.jugador = jugador
    
    @property
    def codigo_de_juego(self):
        return self.__codigo_de_juego
    
    def crear_tablero(self):# se crea el tablero con el que se va a jugar
        return [[' ⚪️ '] * self.__columnas for _ in range(self.__filas)]

    def mostrar_tablero(self):# imprime el tablero
        for i in self.__tablero:
            print(i)
            print()
            
    def actualizar_tablero(self, codigo_adivinar_arreglado,): # actualiza el tablero para mostrar los intentos del jugador
        for i in range(len(codigo_adivinar_arreglado)):
            
            if codigo_adivinar_arreglado[i] == self.__codigo_de_juego[i]:
                self.__tablero[self.__filas - 1][i] = f' 🟢 '
                
            elif codigo_adivinar_arreglado[i] in self.__codigo_de_juego:
                self.__tablero[self.__filas - 1][i] = f' 🟠 '
                
            else:
                self.__tablero[self.__filas - 1][i] = f' ⚪️ '
                
        self.__filas -= 1
            
class Game:
    def __init__(self, computadora, jugador):# recibe las clases de Jugador y computadora
        self.computadora = computadora
        self.jugador = jugador 
        self.__intentos = 0 # Intentos jugados de el jugador
        self.__restante_intentos = 12 #Intentos restantes en retroceso cada que pierda
        self.__codigo_de_juego = None # es none y se cuando el jugador elige ser adivinador o creador 
    
    @property
    def codigo_de_juego(self):
        return self.__codigo_de_juego
    
    @property
    def intentos(self):
        return self.__intentos
    
    @property
    def restante_intentos(self):
        return self.__restante_intentos
    
    def generar_codigo(self):#si jugador es adivinador entonces maquina crea un codigo de juego
        return random.sample(self.computadora.lista_colores, 4)
    
        
    def jugar(self):#Valida si jugador es creador o adivinador
        #si se equivoca entonces el bucle vuelve a funcionar
        while True:
            eleccion = Escoger_Jugador()
            if eleccion == 'Exit':
                print("Has salido del juego.")
                break
            elif eleccion == '1':
                print('\nElegiste ser el creador')
                self.__codigo_de_juego = self.jugador.crear_codigo()
                print("Código de juego creado:", self.__codigo_de_juego)
                break 
            elif eleccion == '2':
                print(f'\n{green}Elegiste ser el adivinador{reset}')
                time.sleep(1) 
                self.__codigo_de_juego = self.generar_codigo()
                print("Generando código de juego...")
                time.sleep(2)   
                print(f"La computadora ha generado un código.\n")
                time.sleep(1)
                x = 3
                for _ in range(x): 
                    print(f"Iniciando partida en {x}")
                    time.sleep(1)
                    x = x - 1
                
                break
            else: 
                print(f"{red}Opción inválida. Elige 1 o 2 o 'Esc' para salir.{reset}")
        
        tablero = Tablero(self.__codigo_de_juego, self.jugador)
        # A la funcion adivinar de la clase Jugador se le mandan como parametros los siguientes datos
        #para poder hacer las validaciones
        while not self.jugador.adivinar(self.__codigo_de_juego, self.__intentos, self.__restante_intentos, tablero):
            self.__restante_intentos -= 1
            self.__intentos += 1
            tablero.mostrar_tablero()
            
        
            
computadora = Computadora(colores)
jugador = Jugador(colores, )
iniciar_juego = Game(computadora, jugador) # se le envian computadura y jugador para que reciba funciones
tablero = Tablero(iniciar_juego.codigo_de_juego, jugador)
iniciar_juego.jugar()


