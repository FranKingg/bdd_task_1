from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .mapa import Mapa
    from .models import Objeto

@dataclass
class Explorador:
    vida: int = 5
    inventario: list["Objeto"] = field(default_factory=list)
    posicion: tuple[int, int] = (0, 0)
    mapa: "Mapa" = None
    dano: int = 10

    def mover(self, direccion: str) -> bool:
        if direccion not in ['norte', 'sur', 'este', 'oeste']:
            return False
        if self.posicion not in self.mapa.habitaciones:
            return False
        
        hab_actual = self.mapa.habitaciones[self.posicion]
        if direccion in hab_actual.conexiones:
            nueva_hab = hab_actual.conexiones[direccion]
            self.posicion = (nueva_hab.x, nueva_hab.y)
            nueva_hab.visitada = True
            return True
        return False

    def explorar_habitacion(self) -> str:
        if self.posicion not in self.mapa.habitaciones:
            return "Error: posición inválida"
        
        hab_actual = self.mapa.habitaciones[self.posicion]
        hab_actual.visitada = True
        
        if hab_actual.contenido:
            return hab_actual.contenido.interactuar(self)
        return "La habitación está vacía."

    def obtener_habitaciones_adyacentes(self) -> list[str]:
        if self.posicion not in self.mapa.habitaciones:
            return []
        return list(self.mapa.habitaciones[self.posicion].conexiones.keys())

    def recibir_dano(self, cantidad: int):
        self.vida -= cantidad
        if self.vida < 0:
            self.vida = 0

    @property
    def esta_vivo(self) -> bool:
        return self.vida > 0
