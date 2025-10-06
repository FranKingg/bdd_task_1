"""Dungeon Generator - Sistema de generación de mapas para dungeons"""

from .models import Habitacion, Objeto
from .contenido import ContenidoHabitacion, Tesoro, Monstruo, Jefe, Evento
from .mapa import Mapa, DIRECCIONES, OPUESTO
from .explorador import Explorador
from .serializacion import guardar_partida, cargar_partida
from .visualizador import Visualizador
from .utils import (
    generar_monstruos_desde_yaml, 
    mostrar_mapa_simple,
    calcular_valor_total_inventario, 
    obtener_habitacion_mas_lejana,
    contar_habitaciones_por_tipo, 
    verificar_conectividad_mapa,
    generar_camino_minimo, 
    crear_mapa_ejemplo,
    obtener_estadisticas_explorador,
    generar_reporte_exploracion,
    calcular_dificultad_habitacion,
    obtener_habitaciones_sin_visitar,
    calcular_porcentaje_completado,
)

__all__ = [
    # Modelos
    "Habitacion", 
    "Objeto", 
    
    # Contenido
    "ContenidoHabitacion", 
    "Tesoro", 
    "Monstruo", 
    "Jefe", 
    "Evento", 
    
    # Mapa
    "Mapa", 
    "DIRECCIONES", 
    "OPUESTO", 
    
    # Explorador
    "Explorador",
    
    # Serialización
    "guardar_partida", 
    "cargar_partida", 
    
    # Visualización
    "Visualizador",
    
    # Utilidades
    "generar_monstruos_desde_yaml", 
    "mostrar_mapa_simple",
    "calcular_valor_total_inventario", 
    "obtener_habitacion_mas_lejana",
    "contar_habitaciones_por_tipo", 
    "verificar_conectividad_mapa",
    "generar_camino_minimo", 
    "crear_mapa_ejemplo",
    "obtener_estadisticas_explorador",
    "generar_reporte_exploracion",
    "calcular_dificultad_habitacion",
    "obtener_habitaciones_sin_visitar",
    "calcular_porcentaje_completado",
]

__version__ = "1.0.0"
