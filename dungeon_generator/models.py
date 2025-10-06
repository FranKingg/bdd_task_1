from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Objeto:
    """Representa un objeto obtenible en el dungeon."""
    nombre: str
    descripcion: str
    valor: int

@dataclass
class Habitacion:
    """Representa una habitación en el dungeon."""
    id: int
    x: int
    y: int
    contenido: Optional["ContenidoHabitacion"] = None
    conexiones: dict[str, "Habitacion"] = field(default_factory=dict)
    visitada: bool = False
    inicial: bool = False
    
    def __hash__(self):
        return hash(self.id)
