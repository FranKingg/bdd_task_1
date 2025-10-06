# Dungeon Generator

Sistema de generación y exploración de dungeons en Python.

## 🚀 Instrucciones de Ejecución

### Requisitos
- Python 3.10 o superior
- Librería `rich` para visualización

### Instalación

```bash
# Navegar al directorio del proyecto
cd dungeon-generator

# Crear entorno virtual
python -m venv .venv

# Activar entorno virtual
# En Linux/macOS:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate

# Instalar dependencias
pip install -e .
```

### Ejecutar el Juego

```bash
python main.py
```

### Uso Básico

1. Selecciona "Nueva partida" en el menú
2. Configura el tamaño del mapa (ej: 10x10) y número de habitaciones (ej: 20)
3. Usa comandos de movimiento: `norte`, `sur`, `este`, `oeste` (o `n`, `s`, `e`, `o`)
4. Explora habitaciones con el comando `explorar` o `ex`
5. Consulta el mapa con `mapa` o `m`
6. Guarda tu progreso con `guardar`

## 📐 Diseño e Implementación

### Arquitectura

El proyecto sigue una arquitectura modular orientada a objetos con separación clara de responsabilidades:

```
dungeon_generator/
├── models.py          # Modelos de datos (Habitacion, Objeto)
├── contenido.py       # Tipos de contenido (Tesoro, Monstruo, Jefe, Evento)
├── mapa.py            # Generación procedural del dungeon
├── explorador.py      # Lógica del jugador
├── visualizador.py    # Interfaz visual con Rich
├── serializacion.py   # Persistencia en JSON
└── utils.py           # Funciones auxiliares
```

### Componentes Principales

**1. Sistema de Generación (mapa.py)**
- Algoritmo de crecimiento orgánico para crear dungeons conectados
- Colocación inteligente de contenido basada en distancia Manhattan
- Garantiza conectividad entre todas las habitaciones

**2. Sistema de Exploración (explorador.py)**
- Movimiento en 4 direcciones con validación
- Sistema de inventario y estadísticas
- Gestión de vida y daño

**3. Sistema de Contenido (contenido.py)**
- Patrón de diseño: Strategy pattern con clase base abstracta `ContenidoHabitacion`
- Monstruos con combate automático
- Tesoros coleccionables
- Jefe final con recompensa especial
- Eventos aleatorios (trampas, curaciones, teletransporte, bonificaciones)

**4. Visualización (visualizador.py)**
- Interfaz rica usando librería Rich
- Mapas coloridos con emojis
- Paneles informativos para habitaciones, estadísticas y estado del explorador

**5. Persistencia (serializacion.py)**
- Serialización completa a JSON
- Preserva estado del mapa, explorador e inventario
- Reconstrucción de conexiones entre habitaciones

### Algoritmos Destacados

- **Generación de Mapa**: Crecimiento aleatorio con validación de límites
- **Distancia Manhattan**: Para calcular lejanía y escalar dificultad
- **BFS (Breadth-First Search)**: Para validar conectividad y encontrar caminos mínimos
- **Distribución de Contenido**: Probabilística basada en porcentajes configurables

### Decisiones de Diseño

1. **Type Hints**: Todo el código usa type hints para mejor mantenibilidad
2. **Dataclasses**: Para modelos de datos limpios y concisos
3. **Herencia**: Contenido usa herencia con ABC para garantizar interfaz consistente
4. **Modularidad**: Cada módulo tiene una responsabilidad única y bien definida
5. **Separación Vista-Lógica**: Visualizador separado de la lógica del juego

## ✅ Cumplimiento de Requerimientos

| # | Requerimiento | Estado | Observaciones |
|---|---------------|--------|---------------|
| 1 | Generación procedural de mapas | ✅ Cumplido | Algoritmo de crecimiento orgánico con validación |
| 2 | Sistema de habitaciones conectadas | ✅ Cumplido | Grafo de habitaciones con conexiones bidireccionales |
| 3 | Múltiples tipos de contenido | ✅ Cumplido | Monstruos, Tesoros, Jefes, Eventos |
| 4 | Sistema de exploración | ✅ Cumplido | Movimiento en 4 direcciones + interacción |
| 5 | Sistema de combate | ✅ Cumplido | Combate automático por turnos |
| 6 | Sistema de inventario | ✅ Cumplido | Objetos coleccionables con valores |
| 7 | Jefe final | ✅ Cumplido | Ubicado en habitación más lejana |
| 8 | Guardado/Cargado de partidas | ✅ Cumplido | Serialización completa en JSON |
| 9 | Visualización del mapa | ✅ Cumplido | Interfaz rica con Rich library |
| 10 | Estadísticas del juego | ✅ Cumplido | Stats de mapa, explorador y progreso |
| 11 | Uso como librería | ✅ Cumplido | API completa exportada en `__init__.py` |
| 12 | Código documentado | ✅ Cumplido | Docstrings en todas las funciones y clases |
| 13 | Type hints | ✅ Cumplido | Type annotations en todo el código |
| 14 | Modularidad | ✅ Cumplido | 7 módulos con responsabilidades claras |
| 15 | Manejo de errores | ✅ Cumplido | Validaciones y excepciones manejadas |

### Requerimientos Adicionales Implementados

| Característica | Estado | Descripción |
|----------------|--------|-------------|
| Sistema de eventos aleatorios | ✅ Cumplido | Trampas, curaciones, teletransporte, bonificaciones |
| Escalado de dificultad | ✅ Cumplido | Enemigos más fuertes lejos del inicio |
| Niebla de guerra | ✅ Cumplido | Habitaciones no visitadas son visualmente diferentes |
| Comandos abreviados | ✅ Cumplido | Atajos para todos los comandos principales |
| Reportes de exploración | ✅ Cumplido | Reporte detallado al finalizar |
| Validación de conectividad | ✅ Cumplido | BFS para verificar que todas las habitaciones sean alcanzables |
| Pathfinding | ✅ Cumplido | Algoritmo de camino mínimo entre habitaciones |
| Utilidades de análisis | ✅ Cumplido | 13+ funciones auxiliares para análisis y debugging |

## 📦 Estructura del Proyecto

```
dungeon-generator/
├── dungeon_generator/
│   ├── __init__.py          # Exportaciones del paquete
│   ├── models.py            # Modelos base (190 líneas)
│   ├── contenido.py         # Contenidos (150 líneas)
│   ├── mapa.py              # Generación del mapa (170 líneas)
│   ├── explorador.py        # Lógica del jugador (60 líneas)
│   ├── visualizador.py      # Visualización (140 líneas)
│   ├── serializacion.py     # Guardado/Cargado (120 líneas)
│   └── utils.py             # Utilidades (210 líneas)
├── main.py                  # Punto de entrada (250 líneas)
├── pyproject.toml          # Configuración del proyecto
├── README.md               # Este archivo
└── .gitignore              # Archivos ignorados

Total: ~1,500 líneas de código
```

## 🎮 Ejemplo de Uso como Librería

```python
from dungeon_generator import Mapa, Explorador, Visualizador

# Crear y configurar mapa
mapa = Mapa(ancho=10, alto=10)
mapa.generar_estructura(n_habitaciones=20)
mapa.colocar_contenido()

# Crear explorador
explorador = Explorador(mapa=mapa)
explorador.posicion = (mapa.habitacion_inicial.x, mapa.habitacion_inicial.y)

# Visualizar
visualizador = Visualizador(mapa)
visualizador.mostrar_mapa_completo(explorador)

# Jugar
explorador.mover('norte')
resultado = explorador.explorar_habitacion()
print(resultado)

# Guardar
from dungeon_generator import guardar_partida
guardar_partida(explorador, "mi_partida.json")
```

## 👤 Autor - FranKingg
 
Proyecto creado como parte de un sistema de generación de dungeons.
