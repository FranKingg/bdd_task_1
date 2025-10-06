"""Utilidades y funciones auxiliares para el dungeon generator."""

from typing import TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from .mapa import Mapa
    from .explorador import Explorador
    from .contenido import Monstruo
    from .models import Habitacion


def generar_monstruos_desde_yaml(archivo: str) -> list["Monstruo"]:
    """
    Genera una lista de monstruos desde un archivo YAML.
    Nota: Esta es una función de ejemplo. Requiere PyYAML instalado.
    """
    from .contenido import Monstruo
    
    monstruos_predefinidos = [
        Monstruo(id=1, nombre="Goblin", vida=15, dano=3),
        Monstruo(id=2, nombre="Orco", vida=25, dano=5),
        Monstruo(id=3, nombre="Esqueleto", vida=20, dano=4),
        Monstruo(id=4, nombre="Zombi", vida=30, dano=6),
        Monstruo(id=5, nombre="Araña Gigante", vida=18, dano=4),
    ]
    
    return monstruos_predefinidos


def mostrar_mapa_simple(mapa: "Mapa", explorador: "Explorador" = None) -> str:
    """
    Genera una representación simple del mapa en formato texto.
    Útil para debugging o visualización sin rich.
    """
    lineas = []
    
    for y in range(mapa.alto):
        fila = []
        for x in range(mapa.ancho):
            pos = (x, y)
            if pos not in mapa.habitaciones:
                fila.append("   ")
            elif explorador and explorador.posicion == pos:
                fila.append(" @ ")
            elif mapa.habitaciones[pos].inicial:
                fila.append(" E ")
            elif mapa.habitaciones[pos].contenido:
                tipo = mapa.habitaciones[pos].contenido.tipo
                if tipo == "Jefe Final":
                    fila.append(" J ")
                elif tipo == "Monstruo":
                    fila.append(" M ")
                elif tipo == "Cofre del Tesoro":
                    fila.append(" T ")
                elif tipo == "Evento":
                    fila.append(" ! ")
                else:
                    fila.append(" · ")
            else:
                fila.append(" · ")
        lineas.append("".join(fila))
    
    leyenda = "\n\nLeyenda: @ = Tú | E = Entrada | J = Jefe | M = Monstruo | T = Tesoro | ! = Evento | · = Vacío"
    return "\n".join(lineas) + leyenda


def calcular_valor_total_inventario(explorador: "Explorador") -> int:
    """Calcula el valor total de todos los objetos en el inventario."""
    return sum(obj.valor for obj in explorador.inventario)


def obtener_habitacion_mas_lejana(mapa: "Mapa", origen: tuple[int, int]) -> tuple[int, int]:
    """
    Encuentra la habitación más lejana del origen usando distancia Manhattan.
    """
    max_dist = -1
    pos_lejana = origen
    
    for pos in mapa.habitaciones.keys():
        dist = abs(pos[0] - origen[0]) + abs(pos[1] - origen[1])
        if dist > max_dist:
            max_dist = dist
            pos_lejana = pos
    
    return pos_lejana


def contar_habitaciones_por_tipo(mapa: "Mapa") -> dict[str, int]:
    """Cuenta cuántas habitaciones hay de cada tipo de contenido."""
    conteo = {
        "Monstruo": 0,
        "Cofre del Tesoro": 0,
        "Jefe Final": 0,
        "Evento": 0,
        "Vacías": 0
    }
    
    for hab in mapa.habitaciones.values():
        if hab.contenido:
            tipo = hab.contenido.tipo
            conteo[tipo] = conteo.get(tipo, 0) + 1
        else:
            conteo["Vacías"] += 1
    
    return conteo


def verificar_conectividad_mapa(mapa: "Mapa") -> bool:
    """
    Verifica si todas las habitaciones del mapa están conectadas
    usando BFS (Breadth-First Search).
    """
    if not mapa.habitaciones:
        return False
    
    if not mapa.habitacion_inicial:
        return False
    
    visitadas = set()
    cola = deque([mapa.habitacion_inicial])
    visitadas.add((mapa.habitacion_inicial.x, mapa.habitacion_inicial.y))
    
    while cola:
        hab_actual = cola.popleft()
        
        for hab_vecina in hab_actual.conexiones.values():
            pos_vecina = (hab_vecina.x, hab_vecina.y)
            if pos_vecina not in visitadas:
                visitadas.add(pos_vecina)
                cola.append(hab_vecina)
    
    return len(visitadas) == len(mapa.habitaciones)


def generar_camino_minimo(mapa: "Mapa", inicio: tuple[int, int], fin: tuple[int, int]) -> list[tuple[int, int]]:
    """
    Genera el camino más corto entre dos habitaciones usando BFS.
    Retorna una lista de posiciones que forman el camino.
    """
    if inicio not in mapa.habitaciones or fin not in mapa.habitaciones:
        return []
    
    if inicio == fin:
        return [inicio]
    
    visitadas = {inicio}
    cola = deque([(inicio, [inicio])])
    
    while cola:
        pos_actual, camino = cola.popleft()
        hab_actual = mapa.habitaciones[pos_actual]
        
        for hab_vecina in hab_actual.conexiones.values():
            pos_vecina = (hab_vecina.x, hab_vecina.y)
            
            if pos_vecina == fin:
                return camino + [pos_vecina]
            
            if pos_vecina not in visitadas:
                visitadas.add(pos_vecina)
                cola.append((pos_vecina, camino + [pos_vecina]))
    
    return []


def crear_mapa_ejemplo() -> "Mapa":
    """Crea un mapa de ejemplo para pruebas rápidas."""
    from .mapa import Mapa
    from .models import Habitacion, Objeto
    from .contenido import Monstruo, Tesoro, Jefe
    
    mapa = Mapa(ancho=5, alto=5)
    
    # Crear habitaciones manualmente
    hab1 = Habitacion(id=0, x=2, y=2, inicial=True)
    hab2 = Habitacion(id=1, x=2, y=1)
    hab3 = Habitacion(id=2, x=3, y=1)
    hab4 = Habitacion(id=3, x=3, y=2)
    hab5 = Habitacion(id=4, x=4, y=2)
    
    # Conectar habitaciones
    hab1.conexiones["norte"] = hab2
    hab2.conexiones["sur"] = hab1
    hab2.conexiones["este"] = hab3
    hab3.conexiones["oeste"] = hab2
    hab3.conexiones["sur"] = hab4
    hab4.conexiones["norte"] = hab3
    hab4.conexiones["este"] = hab5
    hab5.conexiones["oeste"] = hab4
    
    # Añadir contenido
    hab2.contenido = Monstruo(id=100, nombre="Goblin", vida=15, dano=3)
    hab3.contenido = Tesoro(recompensa=Objeto("Espada de Hierro", "Espada básica", 50))
    hab4.contenido = Monstruo(id=101, nombre="Orco", vida=25, dano=5)
    hab5.contenido = Jefe(
        id=999,
        nombre="Rey Goblin",
        vida=50,
        dano=8,
        recompensa_especial=Objeto("Corona Dorada", "Victoria", 1000)
    )
    
    # Añadir al mapa
    mapa.habitaciones[(2, 2)] = hab1
    mapa.habitaciones[(2, 1)] = hab2
    mapa.habitaciones[(3, 1)] = hab3
    mapa.habitaciones[(3, 2)] = hab4
    mapa.habitaciones[(4, 2)] = hab5
    mapa.habitacion_inicial = hab1
    
    return mapa


def obtener_estadisticas_explorador(explorador: "Explorador") -> dict:
    """Obtiene estadísticas detalladas del explorador."""
    return {
        "vida": explorador.vida,
        "dano": explorador.dano,
        "posicion": explorador.posicion,
        "objetos_inventario": len(explorador.inventario),
        "valor_total_inventario": calcular_valor_total_inventario(explorador),
        "esta_vivo": explorador.esta_vivo,
    }


def generar_reporte_exploracion(explorador: "Explorador") -> str:
    """Genera un reporte detallado de la exploración."""
    habitaciones_visitadas = sum(1 for hab in explorador.mapa.habitaciones.values() if hab.visitada)
    total_habitaciones = len(explorador.mapa.habitaciones)
    progreso = (habitaciones_visitadas / total_habitaciones * 100) if total_habitaciones > 0 else 0
    
    lineas = [
        "=" * 50,
        "REPORTE DE EXPLORACIÓN",
        "=" * 50,
        f"Habitaciones exploradas: {habitaciones_visitadas}/{total_habitaciones} ({progreso:.1f}%)",
        f"Vida restante: {explorador.vida}",
        f"Daño actual: {explorador.dano}",
        f"Objetos recolectados: {len(explorador.inventario)}",
        f"Valor total del botín: {calcular_valor_total_inventario(explorador)} oro",
        "=" * 50,
    ]
    
    if explorador.inventario:
        lineas.append("\nINVENTARIO:")
        for i, obj in enumerate(explorador.inventario, 1):
            lineas.append(f"  {i}. {obj.nombre} - {obj.valor} oro")
    
    return "\n".join(lineas)


def calcular_dificultad_habitacion(mapa: "Mapa", posicion: tuple[int, int]) -> str:
    """
    Calcula la dificultad estimada de una habitación basada en su contenido.
    """
    if posicion not in mapa.habitaciones:
        return "Desconocida"
    
    hab = mapa.habitaciones[posicion]
    
    if not hab.contenido:
        return "Segura"
    
    tipo = hab.contenido.tipo
    
    if tipo == "Jefe Final":
        return "Mortal"
    elif tipo == "Monstruo":
        vida = hab.contenido.vida
        if vida < 20:
            return "Fácil"
        elif vida < 30:
            return "Media"
        else:
            return "Difícil"
    elif tipo == "Evento":
        efecto = hab.contenido.efecto
        if efecto in ["trampa"]:
            return "Peligrosa"
        else:
            return "Segura"
    else:
        return "Segura"


def obtener_habitaciones_sin_visitar(mapa: "Mapa") -> list[tuple[int, int]]:
    """Retorna una lista de posiciones de habitaciones no visitadas."""
    return [pos for pos, hab in mapa.habitaciones.items() if not hab.visitada]


def calcular_porcentaje_completado(explorador: "Explorador") -> float:
    """Calcula el porcentaje de completado del dungeon."""
    total = len(explorador.mapa.habitaciones)
    visitadas = sum(1 for hab in explorador.mapa.habitaciones.values() if hab.visitada)
    
    if total == 0:
        return 0.0
    
    return (visitadas / total) * 100
