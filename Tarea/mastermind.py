#                                                Mastermind
import random 
import time
from colored import fg, attr
from itertools import permutations
def main():
    red = fg('red')
    green = fg('green')
    blue = fg('blue')
    magenta = fg('magenta')
    reset = attr('reset')

    colores = ['red', 'blue', 'green', 'yellow',"black", "white"]  # lista de colores que utilizare para todo

    def Escoger_Jugador():
        return input("\nElige (1: Creador, 2: Adivinador, 3: Exit):  ")
    #Jugador escoge si ser adivinador o creador de codigo


    class Computadora:
        def __init__(self, lista_colores): #Funcionalidad de computadora
            self.__lista_colores = lista_colores
            self.__dificultad = None
            self.__codigo_secreto = None #declarados en NONE pq el valor se les da luego
            self.codigoJuego = None
            self.NewSecuencia = ["","","",""]
            self.tablero = None
            
        @property
        def codigo_secreto(self):
            return self.__codigo_secreto
        @property
        def lista_colores(self):
            return self.__lista_colores
        @property
        def dificultad(self):
            return self.__dificultad

        def generar_codigo(self):  # codigo generado por el jugador
            x = input("Ingresa 4 colores separados por comas (ejemplo: red,blue,green,yellow): ")
            return [color.strip() for color in x.split(',')]

        def facil(self):
            return random.sample(self.__lista_colores, k=4)
        
        def medio(self):
            todas_permutaciones = list(permutations(self.__lista_colores, 4))
            return list(random.choice(todas_permutaciones))
        
        def dificil(self):
            if len(self.NewSecuencia) == 4:  # Debe tener 4 espacios para hacer la validación
                x = random.sample(self.__lista_colores, k=4)
                for i in range(len(x)):
                    if x[i] in self.codigoJuego:
                        if x[i] in self.NewSecuencia:
                            pass
                        else:   
                            self.NewSecuencia[self.NewSecuencia.index("")] = x[i]  # Reemplaza el primer espacio vacío
            else:
                for i in range(len(self.NewSecuencia)):
                    if self.NewSecuencia[i] == "":
                        self.NewSecuencia[i] = random.sample(self.__lista_colores)
                        
            for j in self.NewSecuencia:
                if self.NewSecuencia[i] != "":
                    self.NewSecuencia = self.codigoJuego
                    
            return self.NewSecuencia
            
        def elegir_dificultad(self):# elige la dificultad
            while True:
                try:
                    dificultad = int(input("Elige dificultad (1: fácil, 2: medio, 3: dificil): "))
                    if dificultad in [1, 2, 3]:
                        self.__dificultad = dificultad
                        return
                    else:
                        print("Número de dificultad no válido. Debe ser 1, 2 o 3.")
                except ValueError:
                    print("Entrada no válida. Por favor ingresa un número entero.")

        def generar_codigo_secreto(self):
            if self.__dificultad == 1:
                return self.facil()
            elif self.__dificultad == 2:
                return self.medio()
            elif self.__dificultad == 3:
                return self.dificil()
            
        def enviar_adivinacion_pc(self, tablero, codigo_de_juego, intentos, restante_intentos):
            time.sleep(1)
            self.tablero = tablero
            self.codigoJuego = codigo_de_juego
            self.__codigo_secreto = self.generar_codigo_secreto()#self.__codigo_secreto es el metodo que elige para ejecutar los metodos de facil, medio o dificl
            self.tablero.actualizar_tablero(self.__codigo_secreto,)# a actualizar tablero de la class tablero se le envia el codigo creador por la maquina
            #para validarlo
            if self.__codigo_secreto == codigo_de_juego:# si el codigo es exactament igual entonces gana la maquina
                print(f'\n{green}Has perdido! la maquina ha adivinado el código en {intentos} intentos.{reset}')
                print(f'La combinación de colores era {codigo_de_juego}')
                self.tablero.mostrar_tablero()
                return True
            else:
                print(f'\n{red}Intento incorrecto. {restante_intentos} intentos restantes.{reset}')
                # print(f'Su último movimiento fue {green}{self.__codigo_secreto}{reset}\n')
                if restante_intentos <= 1:
                    print("Ganaste, la maquina no ha logrado adivinar!")
                    self.tablero.mostrar_tablero()
                    return True
            return False
    class Jugador:
        def __init__(self, lista_colores):#recibo la lista de colores 
            self.__lista_colores = lista_colores
            self.__comando_lista = [] #guardo cada jugada que hago para llevar un registro

        @property
        def lista_colores(self):
            return self.__lista_colores

        @property
        def comando_lista(self):
            return self.__comando_lista

        def adivinar(self, codigo_de_juego, intentos, restante_intentos, tablero): #recibe los parametros enviados desde la class GAME
            print(f'\nAdivina el código \nOpciones {self.__lista_colores}\n')
            codigo_adivinar = input('Ingresa 4 colores separados por comas (ejemplo: red,blue,green,yellow): ').lower()

            if codigo_adivinar == '/list': # list para ver el historial de jugadas que he hecho
                if not self.__comando_lista:
                    print(f'\n{red}No hay registro disponible{reset}\n')   
                else:
                    print(f'\n{green}- {reset}Tus últimas jugadas fueron:')
                    for i, jugadas in enumerate(self.__comando_lista, 1): #muestra las jugadas iteradas y enumerdas
                        print(f' {green}{i} {reset}{jugadas}')    
                return 'list'
            else:
                codigo_adivinar_arreglado = [color.strip() for color in codigo_adivinar.split(',')]
                self.__comando_lista.append(codigo_adivinar_arreglado) # al array de jugadas le hago un append de mi eleccion actual
                tablero.actualizar_tablero(codigo_adivinar_arreglado)
                tablero.mostrar_tablero(codigo_de_juego) #muestro el tablero

                if codigo_adivinar_arreglado == codigo_de_juego: #valido si he ganado o si he perdido 
                    print(f'\n{green}¡Felicidades! Adivinaste el código en {intentos} intentos.{reset}')
                    print(f'La combinación de colores era {codigo_de_juego}')
                    return True
                else:
                    print(f'\n{red}Intento incorrecto. {restante_intentos - 1} intentos restantes.{reset}')
                    print(f'Tu último movimiento fue {green}{codigo_adivinar_arreglado}{reset}')
                    # print(f'Bola blanca significa que no adivino\nBola Verde significa que no adivino\n')
                
                    
                    if restante_intentos <= 1:
                        print("Perdiste, el juego ha terminado!")
                        print(codigo_de_juego)
                        return True
                    return False 

    class Tablero:
        def __init__(self, codigo_de_juego, jugador, computadora, filas=12, columnas=4):# recibo todos los parametrs desde la class GAME
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
            return [[' O '] * self.__columnas for _ in range(self.__filas)] # multiplico los 1 circulo por el numero de columnas
        # y a el numero de columnas un for de el rango de filas para crear el tablero

        def mostrar_tablero(self,codigo_de_juego):
            
            print()
            print("            Tablero                     Feedback")
            print()
            for fila in self.__tablero:
                time.sleep(0.1)
                print("  ".join(fila) + "   |    " + " ".join(codigo_de_juego)) #muestro el tablero y entre cada fila le pondre una linea para que se vea bonito
                print()
                
        def actualizar_tablero(self, codigo_adivinado):# el codigo de el jugador correspondiente viene de la class GAME y de la class Computadora si es que juega la computadora
            self.__filas -= 1 # va empezar desde la ultima fila y le resta 1 para que se vea que sube a la siguiente oportunidad
            for i in range(len(codigo_adivinado)):
                if codigo_adivinado[i] == self.__codigo_de_juego[i]: # si el codigo_adivinado en la posicion 1 por ejemplo es igual a
                    #codigo de juego en la posicion1 tambien entonces cambia se le setea el color verde
                    self.__tablero[self.__filas][i] = f'{green} O {reset}'
                elif codigo_adivinado[i] in self.__codigo_de_juego:# si existe pero en la posicion incorrecta entonces lo marca como anaranjado
                    self.__tablero[self.__filas][i] = f'{red} O {reset}'
                else:
                    self.__tablero[self.__filas][i] = ' O '# si no en blacno


    class Game:
        def __init__(self, computadora, jugador):#Recibe las instancias de jugador y computadora 
            self.computadora = computadora
            self.jugador = jugador 
            self.__intentos = 1 #definimos los intentos con los que comienza
            self.__restante_intentos = 12 #intentos restantes
            self.__codigo_de_juego = None #comienza en None pq se genera luego

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
            return random.sample(self.computadora.lista_colores, 4) #Genera un codigo random

        def jugar(self):
            while True:
                eleccion = Escoger_Jugador() #Si jugador escribio exit entonces termino el programa
                if eleccion == "3":
                    print("Has salido del juego.")
                    break
                elif eleccion == '1': # Si escogio 1 ejecuta este bloque de creador
                    print(f'\n{green}Elegiste ser el creador{reset}')
                    self.__codigo_de_juego = self.computadora.generar_codigo() #en codigo de juego se guarda la funcion generarCodigo de la instancia computadora y es la class
                    self.computadora.elegir_dificultad() # Se ejecuta de la class computadora el elegir dificultad
                    print("Código de juego creado:", self.__codigo_de_juego)
                    time.sleep(2)
                    tablero = Tablero(self.__codigo_de_juego, self.jugador, self.computadora) # A tabllero se le envian las class computadora y jugador como instancias para hacer validaciones
                    while not self.computadora.enviar_adivinacion_pc(tablero, self.__codigo_de_juego, self.__intentos, self.__restante_intentos):# le paso estos parametros a enviar_adivinacion_pc de class computadora
                        self.__restante_intentos -= 1
                        self.__intentos += 1
                        if self.__restante_intentos <= 0:
                            print("Perdiste, el juego ha terminado!")
                            break
                    # al haber enviado como paramtetro la instancia de computadora puedo usar sus metodos refiriendome a ella, es como el SUPER()
                        tablero.mostrar_tablero()#Muestro e tablero

                elif eleccion == '2': # Si escojo 2 entonces ejecuta este codigo
                    print(f'\n{green}Elegiste ser el adivinador{reset}')
                    time.sleep(1)
                    self.__codigo_de_juego = self.generar_codigo() #genero un codigo random que es el metodo que esta arriba de este metodo jugar():
                    print("Generando código de juego...")
                    time.sleep(2)
                    print(f"La computadora ha generado un código.\n")
                    time.sleep(1)
                    tablero = Tablero(self.__codigo_de_juego, self.jugador, self.computadora)# a tablero le envio las mismas intancias para validaciones
                    while not self.jugador.adivinar(self.__codigo_de_juego, self.__intentos, self.__restante_intentos, tablero): #le envio estos parametros al metodo adivinar
                        self.__restante_intentos -= 1 # contandores incrementan y decrementan cada ronda
                        self.__intentos += 1
                        if self.__restante_intentos <= 0:
                            print("Perdiste, el juego ha terminado!")
                            break
                    break

                else:
                    print(f"{red}Opción inválida. Elige 1 o 2 o 'Exit' para salir.{reset}")
                    #si la eleccione es invalida etnonces vuelve ejecutar el while

    #Se crean instancias de computadora y jugador y se le pasan a GAME para poder usar sus metodos y datos
    computadora = Computadora(colores)
    jugador = Jugador(colores)
    iniciar_juego = Game(computadora, jugador)
    iniciar_juego.jugar()
if __name__ == "__main__":
    main()    