from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from .explorador import Explorador
    from .models import Objeto

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
    def interactuar(self, explorador: "Explorador") -> str:
        pass

@dataclass
class Tesoro(ContenidoHabitacion):
    recompensa: "Objeto"

    @property
    def descripcion(self) -> str:
        return f"Cofre con {self.recompensa.nombre}"

    @property
    def tipo(self) -> str:
        return "Cofre del Tesoro"

    def interactuar(self, explorador: "Explorador") -> str:
        explorador.inventario.append(self.recompensa)
        habitacion_actual = explorador.mapa.habitaciones[explorador.posicion]
        habitacion_actual.contenido = None
        return f"¡Recogiste el tesoro: {self.recompensa.nombre}!"

@dataclass
class Monstruo(ContenidoHabitacion):
    id: int
    nombre: str
    vida: int
    dano: int

    @property
    def descripcion(self) -> str:
        return f"{self.nombre} (Vida: {self.vida}, Daño: {self.dano})"

    @property
    def tipo(self) -> str:
        return "Monstruo"

    def interactuar(self, explorador: "Explorador") -> str:
        resultado = [f"¡Te enfrentas a {self.nombre}!"]
        
        while self.vida > 0 and explorador.esta_vivo:
            if random.randint(0, 1) == 0:
                self.vida -= explorador.dano
                resultado.append(f"Atacas ({explorador.dano} daño)")
                if self.vida > 0:
                    resultado.append(f"Vida del {self.nombre}: {self.vida}")
            else:
                explorador.recibir_dano(self.dano)
                resultado.append(f"{self.nombre} ataca ({self.dano} daño)")
                resultado.append(f"Tu vida: {explorador.vida}")
        
        if self.vida <= 0:
            explorador.mapa.habitaciones[explorador.posicion].contenido = None
            resultado.append(f"¡Derrotaste a {self.nombre}!")
        elif not explorador.esta_vivo:
            resultado.append(f"Fuiste derrotado por {self.nombre}.")
        
        return "\n".join(resultado)

@dataclass
class Jefe(Monstruo):
    recompensa_especial: "Objeto" = None

    @property
    def descripcion(self) -> str:
        return f"JEFE: {self.nombre} (Vida: {self.vida}, Daño: {self.dano})"

    @property
    def tipo(self) -> str:
        return "Jefe Final"

    def interactuar(self, explorador: "Explorador") -> str:
        resultado = [f"¡¡¡BATALLA CONTRA {self.nombre.upper()}!!!"]
        
        while self.vida > 0 and explorador.esta_vivo:
            if random.randint(0, 5) <= 1:
                self.vida -= explorador.dano
                resultado.append(f"Atacas al jefe ({explorador.dano} daño)")
                if self.vida > 0:
                    resultado.append(f"Vida del jefe: {self.vida}")
            else:
                explorador.recibir_dano(self.dano)
                resultado.append(f"El jefe golpea ({self.dano} daño)")
                resultado.append(f"Tu vida: {explorador.vida}")
        
        if self.vida <= 0:
            explorador.mapa.habitaciones[explorador.posicion].contenido = None
            resultado.append(f"¡¡¡DERROTASTE A {self.nombre.upper()}!!!")
            if self.recompensa_especial:
                explorador.inventario.append(self.recompensa_especial)
                resultado.append(f"¡Obtuviste: {self.recompensa_especial.nombre}!")
        elif not explorador.esta_vivo:
            resultado.append(f"Caíste ante {self.nombre}.")
        
        return "\n".join(resultado)

@dataclass
class Evento(ContenidoHabitacion):
    nombre_evento: str
    descripcion_evento: str
    efecto: str
    valor_efecto: int = 0

    @property
    def descripcion(self) -> str:
        return self.descripcion_evento

    @property
    def tipo(self) -> str:
        return "Evento"

    def interactuar(self, explorador: "Explorador") -> str:
        resultado = [f"¡Evento: {self.nombre_evento}!", self.descripcion_evento]
        
        if self.efecto == "trampa":
            explorador.recibir_dano(self.valor_efecto)
            resultado.append(f"Perdiste {self.valor_efecto} vida. Actual: {explorador.vida}")
        elif self.efecto == "curacion":
            explorador.vida += self.valor_efecto
            resultado.append(f"Recuperaste {self.valor_efecto} vida. Actual: {explorador.vida}")
        elif self.efecto == "teletransporte":
            hab_disp = list(explorador.mapa.habitaciones.keys())
            hab_disp.remove(explorador.posicion)
            nueva_pos = random.choice(hab_disp)
            explorador.posicion = nueva_pos
            resultado.append(f"¡Teletransportado a {nueva_pos}!")
        elif self.efecto == "bonificacion":
            explorador.dano += self.valor_efecto
            resultado.append(f"Daño aumentado en {self.valor_efecto}. Actual: {explorador.dano}")
        
        explorador.mapa.habitaciones[explorador.posicion].contenido = None
        return "\n".join(resultado)
