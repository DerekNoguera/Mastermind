#                                                Mastermind
import random 
import time
from colored import fg, attr

red = fg('red')
green = fg('green')
blue = fg('blue')
magenta = fg('magenta')
reset = attr('reset')

colores = ['red', 'blue', 'green', 'yellow',"black", "white"]  # lista de colores

def Escoger_Jugador():
    return input("\nElige 1 para ser el creador \nElige 2 para ser el adivinador \nEscribe 'Exit' para salir:\n")


class Computadora:
    def __init__(self, lista_colores):
        self.__lista_colores = lista_colores
        self.__codigo_secreto = random.sample(self.__lista_colores, k=4)
        self.__dificultad = None
    @property
    def lista_colores(self):
        return self.__lista_colores
    @property
    def dificultad(self):
        return self.__dificultad

    def generar_codigo(self):  
        return input("Ingresa los colores separados por comas (ejemplo: red,blue,green,yellow): ")
    
    def elegir_dificultad(self):
        while True:
            try:
                dificultad = int(input("Elige el nivel de dificultad (1: fácil, 2: medio, 3: alto): "))
                if dificultad in [1, 2, 3]:
                    self.__dificultad = dificultad
                    return
                else:
                    print("Número de dificultad no válido. Debe ser 1, 2 o 3.")
            except ValueError:
                print("Entrada no válida. Por favor ingresa un número entero.")


    
    def enviar_adivinacion_pc(self, tablero, codigo_de_juego, intentos, restante_intentos):
        time.sleep(1)
        self.__codigo_secreto = random.sample(self.__lista_colores, k=4) 
        if self.__codigo_secreto == codigo_de_juego:
            print(f'\n{green}Has perdido! la maquina ha adivinado el código en {intentos} intentos.{reset}')
            print(f'La combinación de colores era {codigo_de_juego}')
            return True
        else:
            print(f'\n{red}Intento incorrecto. {restante_intentos} intentos restantes.{reset}')
            print(f'Su último movimiento fue {green}{self.__codigo_secreto}{reset}\n')
                
            if restante_intentos <= 1:
                print("Ganaste, la maquina no ha logrado adivinar!")
                return True
        tablero.actualizar_tablero(self.__codigo_secreto)
        return False

    

class Jugador:
    def __init__(self, lista_colores):
        self.__lista_colores = lista_colores
        self.__comando_lista = []

    @property
    def lista_colores(self):
        return self.__lista_colores

    @property
    def comando_lista(self):
        return self.__comando_lista

    def adivinar(self, codigo_de_juego, intentos, restante_intentos, tablero):
        print(f'\nAdivina el código \nOpciones {self.__lista_colores}\n')
        codigo_adivinar = input('Ingresa los colores separados por comas (ejemplo: red,blue,green,yellow): ').lower()

        if codigo_adivinar == '/list':
            if not self.__comando_lista:
                print(f'\n{red}No hay registro disponible{reset}\n')   
            else:
                print(f'\n{green}- {reset}Tus últimas jugadas fueron:')
                for i, jugadas in enumerate(self.__comando_lista, 1):
                    print(f' {green}{i} {reset}{jugadas}')    
            return 'list'
        else:
            codigo_adivinar_arreglado = [color.strip() for color in codigo_adivinar.split(',')]
            self.__comando_lista.append(codigo_adivinar_arreglado)
            tablero.actualizar_tablero(codigo_adivinar_arreglado)
            tablero.mostrar_tablero()

            if codigo_adivinar_arreglado == codigo_de_juego:
                print(f'\n{green}¡Felicidades! Adivinaste el código en {intentos} intentos.{reset}')
                print(f'La combinación de colores era {codigo_de_juego}')
                return True
            else:
                print(f'\n{red}Intento incorrecto. {restante_intentos - 1} intentos restantes.{reset}')
                print(f'Tu último movimiento fue {green}{codigo_adivinar_arreglado}{reset}\n')
                
                if restante_intentos <= 1:
                    print("Perdiste, el juego ha terminado!")
                    print(codigo_de_juego)
                    return True
                return False

class Tablero:
    def __init__(self, codigo_de_juego, jugador, computadora, filas=12, columnas=4):
        self.__filas = filas
        self.__columnas = columnas
        self.__codigo_de_juego = codigo_de_juego
        self.__tablero = self.crear_tablero()
        self.jugador = jugador
        self.computadora = computadora

    @property
    def codigo_de_juego(self):
        return self.__codigo_de_juego

    def crear_tablero(self):
        return [[' ⚪️ '] * self.__columnas for _ in range(self.__filas)]

    def mostrar_tablero(self):
        print()
        for fila in self.__tablero:
            print(" | ".join(fila))
            print()
    def actualizar_tablero(self, codigo_adivinado):
        self.__filas -= 1
        for i in range(len(codigo_adivinado)):
            if codigo_adivinado[i] == self.__codigo_de_juego[i]:
                self.__tablero[self.__filas][i] = ' 🟢 '
            elif codigo_adivinado[i] in self.__codigo_de_juego:
                self.__tablero[self.__filas][i] = ' 🟠 '
            else:
                self.__tablero[self.__filas][i] = ' ⚪️ '
        

class Game:
    def __init__(self, computadora, jugador):
        self.computadora = computadora
        self.jugador = jugador 
        self.__intentos = 1
        self.__restante_intentos = 12
        self.__codigo_de_juego = None

    @property
    def codigo_de_juego(self):
        return self.__codigo_de_juego

    @property
    def intentos(self):
        return self.__intentos

    @property
    def restante_intentos(self):
        return self.__restante_intentos

    def generar_codigo(self):
        return random.sample(self.computadora.lista_colores, 4)

    def jugar(self):
        while True:
            eleccion = Escoger_Jugador()
            if eleccion == 'Exit':
                print("Has salido del juego.")
                break
            elif eleccion == '1':
                print(f'\n{green}Elegiste ser el creador{reset}')
                self.__codigo_de_juego = self.computadora.generar_codigo()
                self.computadora.elegir_dificultad()
                print("Código de juego creado:", self.__codigo_de_juego)
                time.sleep(2)
                tablero = Tablero(self.__codigo_de_juego, self.jugador, self.computadora)
                while not self.computadora.enviar_adivinacion_pc(tablero, self.__codigo_de_juego, self.__intentos, self.__restante_intentos):
                    self.__restante_intentos -= 1
                    self.__intentos += 1
                    if self.__restante_intentos <= 0:
                        print("Perdiste, el juego ha terminado!")
                        break

                    tablero.mostrar_tablero()

            elif eleccion == '2':
                print(f'\n{green}Elegiste ser el adivinador{reset}')
                time.sleep(1)
                self.__codigo_de_juego = self.generar_codigo()
                print("Generando código de juego...")
                time.sleep(2)
                print(f"La computadora ha generado un código.\n")
                time.sleep(1)
                # self.__restante_intentos = self.computadora.dificultad() 
                tablero = Tablero(self.__codigo_de_juego, self.jugador, self.computadora)
                while not self.jugador.adivinar(self.__codigo_de_juego, self.__intentos, self.__restante_intentos, tablero):
                    self.__restante_intentos -= 1
                    self.__intentos += 1
                    if self.__restante_intentos <= 0:
                        print("Perdiste, el juego ha terminado!")
                        break
                break

            else:
                print(f"{red}Opción inválida. Elige 1 o 2 o 'Exit' para salir.{reset}")


computadora = Computadora(colores)
jugador = Jugador(colores)
iniciar_juego = Game(computadora, jugador)
iniciar_juego.jugar()
