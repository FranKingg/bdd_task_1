from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Optional
import random

def main():
    print("Hello from task-1!")


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
    habitacion_inicial: Habitacion # donde empieza el explorador

    def generar_estructura(self, n_habitaciones: int):
        pass
        
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
        contenido = self.mapa.habitaciones[self.posicion].contenido # Obtener el contenido de la habitación actual
        
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

    def interactuar(self, explorador = Explorador) -> str:
        return f"Evento ocurrido: {self.descripcion_evento}"
    
def num_ale_prob() -> int:
    return random.randint(0, 100)

def num_ale(min: int, max: int) -> int:
    return random.randint(min, max)

if __name__ == "__main__":
    main()