from dataclasses import dataclass, field
from typing import Optional
import random
from .models import Habitacion, Objeto
from .contenido import Tesoro, Monstruo, Jefe, Evento

DIRECCIONES = {"norte": (0, -1), "sur": (0, 1), "este": (1, 0), "oeste": (-1, 0)}
OPUESTO = {"norte": "sur", "sur": "norte", "este": "oeste", "oeste": "este"}

@dataclass
class Mapa:
    ancho: int
    alto: int
    habitaciones: dict[tuple[int, int], Habitacion] = field(default_factory=dict)
    habitacion_inicial: Optional[Habitacion] = None

    def generar_estructura(self, n_habitaciones: int) -> str:
        if n_habitaciones < 1 or n_habitaciones > self.ancho * self.alto:
            return f"Error: inválido. Debe ser entre 1 y {self.ancho * self.alto}"
        
        self.habitaciones.clear()
        self.habitacion_inicial = None
        
        lado = random.choice(['norte', 'sur', 'este', 'oeste'])
        if lado == 'norte':
            x_inicial, y_inicial = random.randint(0, self.ancho - 1), 0
        elif lado == 'sur':
            x_inicial, y_inicial = random.randint(0, self.ancho - 1), self.alto - 1
        elif lado == 'este':
            x_inicial, y_inicial = self.ancho - 1, random.randint(0, self.alto - 1)
        else:
            x_inicial, y_inicial = 0, random.randint(0, self.alto - 1)
        
        self.habitacion_inicial = Habitacion(
            id=0, x=x_inicial, y=y_inicial, inicial=True
        )
        self.habitaciones[(x_inicial, y_inicial)] = self.habitacion_inicial
        
        id_hab = 1
        sin_progreso = 0
        
        while len(self.habitaciones) < n_habitaciones:
            pos_actual = random.choice(list(self.habitaciones.keys()))
            x_actual, y_actual = pos_actual
            direcciones = list(DIRECCIONES.keys())
            random.shuffle(direcciones)
            
            creada = False
            for direccion in direcciones:
                dx, dy = DIRECCIONES[direccion]
                nx, ny = x_actual + dx, y_actual + dy
                
                if 0 <= nx < self.ancho and 0 <= ny < self.alto:
                    if (nx, ny) not in self.habitaciones:
                        nueva = Habitacion(id=id_hab, x=nx, y=ny)
                        self.habitaciones[(nx, ny)] = nueva
                        
                        hab_act = self.habitaciones[pos_actual]
                        hab_act.conexiones[direccion] = nueva
                        nueva.conexiones[OPUESTO[direccion]] = hab_act
                        
                        id_hab += 1
                        creada = True
                        sin_progreso = 0
                        break
            
            if not creada:
                sin_progreso += 1
                if sin_progreso > 20:
                    return "Error: no se pudo generar"
        
        return "Estructura generada con éxito."

    def calcular_distancia_manhattan(self, pos1, pos2) -> int:
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def colocar_contenido(self):
        if not self.habitacion_inicial:
            return "Error: sin habitación inicial"
        
        pos_inicial = (self.habitacion_inicial.x, self.habitacion_inicial.y)
        hab_disp = [p for p in self.habitaciones.keys() if p != pos_inicial]
        
        if not hab_disp:
            return "Error: sin habitaciones suficientes"
        
        distancias = {p: self.calcular_distancia_manhattan(pos_inicial, p) for p in hab_disp}
        max_dist = max(distancias.values()) if distancias else 1
        
        pos_jefe = max(hab_disp, key=lambda p: distancias[p])
        hab_disp.remove(pos_jefe)
        
        factor = distancias[pos_jefe] / max_dist if max_dist > 0 else 1
        vida_jefe = int(50 + 50 * factor)
        dano_jefe = int(15 + 15 * factor)
        
        self.habitaciones[pos_jefe].contenido = Jefe(
            id=9999, nombre="Señor Oscuro", vida=vida_jefe, dano=dano_jefe,
            recompensa_especial=Objeto("Corona del Conquistador", "Victoria", 1000)
        )
        
        n_rest = len(hab_disp)
        n_mons = int(n_rest * random.uniform(0.20, 0.30))
        n_tes = int(n_rest * random.uniform(0.15, 0.25))
        n_ev = int(n_rest * random.uniform(0.05, 0.10))
        
        random.shuffle(hab_disp)
        
        for i in range(min(n_mons, len(hab_disp))):
            pos = hab_disp[i]
            fac = distancias[pos] / max_dist if max_dist > 0 else 0.5
            self.habitaciones[pos].contenido = Monstruo(
                id=1000+i,
                nombre=random.choice(["Goblin","Orco","Esqueleto","Zombi","Araña"]),
                vida=int(20+30*fac), dano=int(5+10*fac)
            )
        
        for i in range(n_mons, min(n_mons+n_tes, len(hab_disp))):
            pos = hab_disp[i]
            fac = distancias[pos] / max_dist if max_dist > 0 else 0.5
            self.habitaciones[pos].contenido = Tesoro(
                recompensa=Objeto(
                    random.choice(["Oro","Gema","Espada","Armadura","Poción"]),
                    "Tesoro valioso", int(50+150*fac)
                )
            )
        
        inicio_ev = n_mons + n_tes
        for i in range(inicio_ev, min(inicio_ev+n_ev, len(hab_disp))):
            pos = hab_disp[i]
            tipo = random.choice(['trampa','curacion','teletransporte','bonificacion'])
            
            if tipo == 'trampa':
                ev = Evento("Trampa", "¡Trampa activada!", "trampa", random.randint(1,3))
            elif tipo == 'curacion':
                ev = Evento("Fuente", "Agua cristalina", "curacion", random.randint(2,5))
            elif tipo == 'teletransporte':
                ev = Evento("Portal", "Te absorbe", "teletransporte")
            else:
                ev = Evento("Altar", "Aumenta fuerza", "bonificacion", random.randint(1,3))
            
            self.habitaciones[pos].contenido = ev
        
        return "Contenido colocado."

    def obtener_estadisticas_mapa(self) -> dict:
        total = len(self.habitaciones)
        conteo = {"Monstruo":0, "Cofre del Tesoro":0, "Jefe Final":0, "Evento":0, "Vacías":0}
        total_con = 0
        
        for hab in self.habitaciones.values():
            total_con += len(hab.conexiones)
            if hab.contenido:
                conteo[hab.contenido.tipo] = conteo.get(hab.contenido.tipo, 0) + 1
            else:
                conteo["Vacías"] += 1
        
        return {
            "total_habitaciones": total,
            "monstruos": conteo["Monstruo"],
            "tesoros": conteo["Cofre del Tesoro"],
            "jefes": conteo["Jefe Final"],
            "eventos": conteo["Evento"],
            "vacias": conteo["Vacías"],
            "promedio_conexiones": round(total_con/total if total>0 else 0, 2)
        }
