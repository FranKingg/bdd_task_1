"""Módulo para serializar y deserializar el estado del juego."""

import json
from typing import Optional
from .models import Habitacion, Objeto
from .contenido import Tesoro, Monstruo, Jefe, Evento
from .mapa import Mapa
from .explorador import Explorador


def guardar_partida(explorador: Explorador, archivo: str = "partida.json") -> str:
    """Guarda el estado actual del juego en un archivo JSON."""
    datos = {
        "explorador": {
            "vida": explorador.vida,
            "dano": explorador.dano,
            "posicion": list(explorador.posicion),
            "inventario": [
                {"nombre": obj.nombre, "descripcion": obj.descripcion, "valor": obj.valor}
                for obj in explorador.inventario
            ]
        },
        "mapa": {
            "ancho": explorador.mapa.ancho,
            "alto": explorador.mapa.alto,
            "habitacion_inicial": [
                explorador.mapa.habitacion_inicial.x,
                explorador.mapa.habitacion_inicial.y
            ] if explorador.mapa.habitacion_inicial else None,
            "habitaciones": []
        }
    }
    
    for pos, hab in explorador.mapa.habitaciones.items():
        hab_datos = {
            "id": hab.id,
            "x": hab.x,
            "y": hab.y,
            "visitada": hab.visitada,
            "inicial": hab.inicial,
            "conexiones": list(hab.conexiones.keys()),
            "contenido": None
        }
        
        if hab.contenido:
            if isinstance(hab.contenido, Jefe):
                hab_datos["contenido"] = {
                    "tipo": "Jefe",
                    "id": hab.contenido.id,
                    "nombre": hab.contenido.nombre,
                    "vida": hab.contenido.vida,
                    "dano": hab.contenido.dano,
                    "recompensa_especial": {
                        "nombre": hab.contenido.recompensa_especial.nombre,
                        "descripcion": hab.contenido.recompensa_especial.descripcion,
                        "valor": hab.contenido.recompensa_especial.valor
                    } if hab.contenido.recompensa_especial else None
                }
            elif isinstance(hab.contenido, Monstruo):
                hab_datos["contenido"] = {
                    "tipo": "Monstruo",
                    "id": hab.contenido.id,
                    "nombre": hab.contenido.nombre,
                    "vida": hab.contenido.vida,
                    "dano": hab.contenido.dano
                }
            elif isinstance(hab.contenido, Tesoro):
                hab_datos["contenido"] = {
                    "tipo": "Tesoro",
                    "recompensa": {
                        "nombre": hab.contenido.recompensa.nombre,
                        "descripcion": hab.contenido.recompensa.descripcion,
                        "valor": hab.contenido.recompensa.valor
                    }
                }
            elif isinstance(hab.contenido, Evento):
                hab_datos["contenido"] = {
                    "tipo": "Evento",
                    "nombre_evento": hab.contenido.nombre_evento,
                    "descripcion_evento": hab.contenido.descripcion_evento,
                    "efecto": hab.contenido.efecto,
                    "valor_efecto": hab.contenido.valor_efecto
                }
        
        datos["mapa"]["habitaciones"].append(hab_datos)
    
    with open(archivo, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    
    return f"Partida guardada en {archivo}"


def cargar_partida(archivo: str = "partida.json") -> Optional[Explorador]:
    """Carga una partida guardada desde un archivo JSON."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            datos = json.load(f)
        
        # Crear el mapa
        mapa = Mapa(
            ancho=datos["mapa"]["ancho"],
            alto=datos["mapa"]["alto"]
        )
        
        # Reconstruir habitaciones
        habitaciones_temp = {}
        for hab_datos in datos["mapa"]["habitaciones"]:
            hab = Habitacion(
                id=hab_datos["id"],
                x=hab_datos["x"],
                y=hab_datos["y"],
                visitada=hab_datos["visitada"],
                inicial=hab_datos["inicial"]
            )
            habitaciones_temp[(hab.x, hab.y)] = hab
            mapa.habitaciones[(hab.x, hab.y)] = hab
            
            if hab.inicial:
                mapa.habitacion_inicial = hab
        
        # Reconstruir conexiones
        for hab_datos in datos["mapa"]["habitaciones"]:
            hab = mapa.habitaciones[(hab_datos["x"], hab_datos["y"])]
            for dir_nombre in hab_datos["conexiones"]:
                # Buscar la habitación vecina
                from .mapa import DIRECCIONES
                dx, dy = DIRECCIONES[dir_nombre]
                pos_vecino = (hab.x + dx, hab.y + dy)
                if pos_vecino in mapa.habitaciones:
                    hab.conexiones[dir_nombre] = mapa.habitaciones[pos_vecino]
        
        # Reconstruir contenido
        for hab_datos in datos["mapa"]["habitaciones"]:
            if hab_datos["contenido"]:
                hab = mapa.habitaciones[(hab_datos["x"], hab_datos["y"])]
                cont_datos = hab_datos["contenido"]
                
                if cont_datos["tipo"] == "Jefe":
                    recompensa = None
                    if cont_datos["recompensa_especial"]:
                        recompensa = Objeto(**cont_datos["recompensa_especial"])
                    hab.contenido = Jefe(
                        id=cont_datos["id"],
                        nombre=cont_datos["nombre"],
                        vida=cont_datos["vida"],
                        dano=cont_datos["dano"],
                        recompensa_especial=recompensa
                    )
                elif cont_datos["tipo"] == "Monstruo":
                    hab.contenido = Monstruo(
                        id=cont_datos["id"],
                        nombre=cont_datos["nombre"],
                        vida=cont_datos["vida"],
                        dano=cont_datos["dano"]
                    )
                elif cont_datos["tipo"] == "Tesoro":
                    hab.contenido = Tesoro(
                        recompensa=Objeto(**cont_datos["recompensa"])
                    )
                elif cont_datos["tipo"] == "Evento":
                    hab.contenido = Evento(
                        nombre_evento=cont_datos["nombre_evento"],
                        descripcion_evento=cont_datos["descripcion_evento"],
                        efecto=cont_datos["efecto"],
                        valor_efecto=cont_datos["valor_efecto"]
                    )
        
        # Crear explorador
        explorador = Explorador(
            vida=datos["explorador"]["vida"],
            dano=datos["explorador"]["dano"],
            posicion=tuple(datos["explorador"]["posicion"]),
            mapa=mapa,
            inventario=[Objeto(**obj) for obj in datos["explorador"]["inventario"]]
        )
        
        return explorador
        
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error al cargar partida: {e}")
        return None
