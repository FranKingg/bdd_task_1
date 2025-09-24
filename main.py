from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
from pathlib import Path
import random


# Direcciones y opuestos
DIRECCIONES = {
    "norte": (0, -1),
    "sur":   (0,  1),
    "este":  (1,  0),
    "oeste": (-1, 0),
}

OPUESTO = {"norte": "sur", "sur": "norte", "este": "oeste", "oeste": "este"}

@dataclass
class Habitacion:
    id: int # identificador unico
    x: int # coordenadas en el mapa x
    y: int # coordenadas en el mapa y
    contenido: Optional["ContenidoHabitacion"] # Puede ser None
    conexiones: dict[str, "Habitacion"]  # 'norte', 'sur', 'este', 'oeste' -> Habitacion
    visitada: bool # si la ha visitado el explorador

@dataclass
class Mapa():
    ancho: int #
    alto: int # dimensiones del mapa 
    habitaciones: dict[tuple[int, int], Habitacion]  # (x,y) -> Habitacion
    habitacion_inicial: Optional[Habitacion] # donde empieza el explorador le ponemos optional para que pueda ser None y podamos resetear el mapa

    def generar_estructura(self, n_habitaciones: int):
        if n_habitaciones < 1 or n_habitaciones > self.ancho * self.alto:
            return f"Error: número de habitaciones inválido. debe ser entre 1 y {self.ancho * self.alto}"
        
        self.habitaciones.clear()
        self.habitacion_inicial = None  # Reiniciar la habitacion inicial

        # Generar la primera habitacion en una posicion random del borde del mapa
        # Elegir un borde válido
        lado = random.choice(("arriba", "abajo", "izquierda", "derecha")) # Elegir un lado del borde
        if lado in ("arriba", "abajo"): 
            x_random = random.randint(0, self.ancho - 1) # Elegir una posicion random en el borde
            y_random = 0 if lado == "arriba" else self.alto - 1 # si es arriba y abajo
        else:
            y_random = random.randint(0, self.alto - 1) # Elegir una posicion random en el borde
            x_random = 0 if lado == "izquierda" else self.ancho - 1 # si es izquierda o derecha
        
        self.habitacion_inicial = Habitacion(
            id=1,
            x=x_random,
            y=y_random,
            contenido=None,
            conexiones={},
            visitada=False
        ) # crear la primera habitacion

        self.habitaciones[(x_random, y_random)] = self.habitacion_inicial # añadir la primera habitacion al mapa
        cordenadas_habitacion_inicial = (x_random, y_random) # cursor para moverse por el mapa
        siguiente_id = 2  # id para la siguiente habitacion
        sin_progreso = 0 # contador para evitar atascos

        while len(self.habitaciones) < n_habitaciones:
            direccion = random.choice(list(DIRECCIONES.keys()))
            dx, dy = DIRECCIONES[direccion]
            nueva_x = cordenadas_habitacion_inicial[0] + dx
            nueva_y = cordenadas_habitacion_inicial[1] + dy

            if 0 <= nueva_x < self.ancho and 0 <= nueva_y < self.alto:
                if (nueva_x, nueva_y) not in self.habitaciones:
                    nueva_habitacion = Habitacion(
                        id=siguiente_id,
                        x=nueva_x,
                        y=nueva_y,
                        contenido=None,
                        conexiones={},
                        visitada=False
                    )
                    self.habitaciones[(nueva_x, nueva_y)] = nueva_habitacion
                    siguiente_id += 1

                    # Conectar ambas
                    habitacion_actual = self.habitaciones[cordenadas_habitacion_inicial]
                    habitacion_actual.conexiones[direccion] = nueva_habitacion
                    nueva_habitacion.conexiones[OPUESTO[direccion]] = habitacion_actual

                    sin_progreso = 0
                else:
                    sin_progreso += 1

                #MOVER SIEMPRE EL CURSOR cuando la posición es válida (exista o no la habitación)
                cordenadas_habitacion_inicial = (nueva_x, nueva_y)

                #Anti-atasco por “muchos pasos sin crear”
                if sin_progreso > 10:
                    cordenadas_habitacion_inicial = random.choice(list(self.habitaciones.keys()))
                    sin_progreso = 0

            else:
                # Posición inválida → saltar a otra habitación ya creada
                cordenadas_habitacion_inicial = random.choice(list(self.habitaciones.keys()))
                sin_progreso = 0

        return "Estructura del mapa generada con éxito."


    def colocar_contenido(self):
        pass

@dataclass
class Objeto:


    nombre: str
    descripcion: str
    valor: int

@dataclass
class Explorador:
    vida: int
    inventario: list[Objeto]
    posicion: tuple[int, int]  # (x,y)
    mapa: Mapa
    dano: int

    def mover(self, direccion: str) -> bool:

        actual = self.mapa.habitaciones[self.posicion] # Habitacion actual

        if direccion not in ['norte', 'sur', 'este', 'oeste']: #si la direccion no es valida
            return False # Direccion no valida

        if direccion in actual.conexiones: # Si la direccion es valida
            nueva_habitacion = actual.conexiones[direccion] # Obtener la nueva habitacion
            self.posicion = (nueva_habitacion.x, nueva_habitacion.y) # Actualizar la posicion
            nueva_habitacion.visitada = True # Marcar la habitacion como visitada
            return True # Movimiento exitoso
        return False # Direccion no valida, no se mueve

    def explorar_habitacion(self) -> str:

        habitacion_actual = self.mapa.habitaciones[self.posicion]
        habitacion_actual.visitada = True
        contenido = habitacion_actual.contenido

        if contenido:
            return contenido.interactuar(self)
    
        return "La habitación está vacía."


    def obtener_habitaciones_adyacentes(self) -> list[str]:
        actual = self.mapa.habitaciones[self.posicion] # Habitacion actual
        return list(actual.conexiones.keys()) # Devuelve las direcciones de las habitaciones adyacentes

    
    def recibir_dano(self, cantidad: int):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    @property
    def esta_vivo(self) -> bool:
        if self.vida > 0:
            return True
        return False

class ContenidoHabitacion(ABC):
    @property
    @abstractmethod
    def descripcion(self) -> str:
        pass

    @property
    @abstractmethod
    def tipo(self) -> str:
        pass

    @abstractmethod
    def interactuar(self, explorador: Explorador) -> str:
        pass

@dataclass
class Tesoro(ContenidoHabitacion):
    recompensa: Objeto

    @property
    def descripcion(self) -> str:
        return f"Cofre con {self.recompensa.nombre}"

    @property
    def tipo(self) -> str:
        return "Cofre del Tesoro"

    def interactuar(self, explorador: Explorador) -> str:
        explorador.inventario.append(self.recompensa)
        # dejar la habitación sin contenido
        # (encuéntrala vía mapa y posición del explorador)
        habitacion_actual = explorador.mapa.habitaciones[explorador.posicion]
        habitacion_actual.contenido = None
        
        return f"Recogiste el tesoro: {self.recompensa.nombre}. ¡Felicidades!"


@dataclass
class Monstruo(ContenidoHabitacion):
    nombre: str
    vida: int
    dano: int

    @property
    def descripcion(self) -> str:
        return f"el nombre del monstruo es {self.nombre}, tiene {self.vida} puntos de vida y hace {self.dano} puntos de daño"

    @property
    def tipo(self) -> str:
        return "Monstruo"

    def interactuar(self, explorador: Explorador) -> str:

        while self.vida > 0 and explorador.esta_vivo: # Mientras ambos estén vivos

            prob = num_ale(0,1) # Probabilidad de 50% para cada uno

            if prob == 0: 
                self.vida -= explorador.dano # El explorador hace dano
            elif prob == 1:
                explorador.recibir_dano(self.dano)  # El monstruo hace daño

            if self.vida <= 0: # El monstruo ha muerto
                return f"Has derrotado al monstruo: {self.nombre}. ¡Enhorabuena!"
            pass
            if not explorador.esta_vivo: # El explorador ha muerto
                return "Has sido derrotado por el monstruo. Fin del juego."
            
        return "El combate ha terminado."

@dataclass
class Jefe(Monstruo):

    recompensa_especial: Objeto

    @property
    def descripcion(self) -> str:
        return f"Este jefe es {self.nombre}, tiene {self.vida} puntos de vida, hace {self.dano} puntos de daño y al derrotarlo obtendrás {self.recompensa_especial.nombre}"

    @property
    def tipo(self) -> str:
        return "Jefe final"

    def interactuar(self, explorador: Explorador) -> str:
        
        while self.vida > 0 and explorador.esta_vivo: # Mientras ambos estén vivos

            prob = num_ale(0,5)

            if prob <= 1: # El explorador hace dano
                self.vida -= explorador.dano # El explorador hace dano
            elif prob > 1: # El monstruo hace dano
                explorador.recibir_dano(self.dano)  # El monstruo hace daño

            if self.vida <= 0: # El jefe ha muerto
                return f"Has derrotado al jefe: {self.nombre}. ¡Enhorabuena!"
            if not explorador.esta_vivo: # El explorador ha muerto
                return "Has sido derrotado por el monstruo. Fin del juego."
        
        return "El combate ha terminado."


@dataclass
class Evento(ContenidoHabitacion):
    nombre_evento: str
    descripcion_evento: str
    efecto: str
    @property
    def descripcion(self) -> str:
        return self.descripcion_evento

    @property
    def tipo(self) -> str:
        return "evento"

    def interactuar(self, explorador: Explorador) -> str:
        return f"Evento ocurrido: {self.descripcion_evento}"
    
def num_ale_prob() -> int:
    return random.randint(0, 100)

def num_ale(min: int, max: int) -> int:
    return random.randint(min, max)

def mostrar_mapa(mapa: Mapa):
    print("Mapa generado:")
    for y in range(mapa.alto):
        for x in range(mapa.ancho):
            if (x, y) in mapa.habitaciones:
                if mapa.habitacion_inicial and (x, y) == (mapa.habitacion_inicial.x, mapa.habitacion_inicial.y):
                    print("I", end=" ")  # I para habitación inicial
                else:
                    print("H", end=" ")  # H para habitación
            else:
                print(".", end=" ")  # Espacio vacío
        print()  # salto de línea por fila

def main():
    print("Iniciando el generador de mapas...")
    mapa = Mapa(ancho=10, alto=10, habitaciones={}, habitacion_inicial=None)
    resultado = mapa.generar_estructura(n_habitaciones=40)
    print(resultado)
    mostrar_mapa(mapa)

        
if __name__ == "__main__":
    main()