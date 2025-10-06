"""Módulo para visualización del mapa en la terminal."""

from typing import TYPE_CHECKING
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

if TYPE_CHECKING:
    from .mapa import Mapa
    from .explorador import Explorador


class Visualizador:
    """Clase para visualizar el mapa del dungeon en la terminal."""
    
    def __init__(self, mapa: "Mapa"):
        self.mapa = mapa
        self.console = Console()
    
    def mostrar_mapa_completo(self, explorador: "Explorador" = None):
        """Muestra el mapa completo con todos los detalles."""
        tabla = Table(show_header=False, show_edge=True, padding=(0, 1))
        
        for _ in range(self.mapa.ancho):
            tabla.add_column(justify="center")
        
        for y in range(self.mapa.alto):
            fila = []
            for x in range(self.mapa.ancho):
                celda = self._crear_celda(x, y, explorador)
                fila.append(celda)
            tabla.add_row(*fila)
        
        panel = Panel(
            tabla,
            title="[bold cyan]🗺️  MAPA DEL DUNGEON[/bold cyan]",
            border_style="cyan"
        )
        self.console.print(panel)
    
    def _crear_celda(self, x: int, y: int, explorador: "Explorador" = None) -> Text:
        """Crea el contenido de una celda del mapa."""
        pos = (x, y)
        
        # Celda vacía
        if pos not in self.mapa.habitaciones:
            return Text("   ", style="dim")
        
        hab = self.mapa.habitaciones[pos]
        simbolo = "·"
        color = "white"
        
        # Determinar símbolo y color
        if explorador and explorador.posicion == pos:
            simbolo = "👤"
            color = "bold yellow"
        elif hab.inicial:
            simbolo = "🏠"
            color = "green"
        elif hab.contenido:
            tipo = hab.contenido.tipo
            if tipo == "Jefe Final":
                simbolo = "👑"
                color = "bold red"
            elif tipo == "Monstruo":
                simbolo = "👾"
                color = "red"
            elif tipo == "Cofre del Tesoro":
                simbolo = "💎"
                color = "yellow"
            elif tipo == "Evento":
                simbolo = "❗"
                color = "magenta"
        else:
            simbolo = "·"
            color = "white"
        
        # Marcar si está visitada
        if not hab.visitada and explorador:
            color = f"dim {color}"
        
        return Text(f" {simbolo} ", style=color)
    
    def mostrar_habitacion_actual(self, explorador: "Explorador"):
        """Muestra detalles de la habitación actual."""
        if explorador.posicion not in self.mapa.habitaciones:
            self.console.print("[red]Error: posición inválida[/red]")
            return
        
        hab = self.mapa.habitaciones[explorador.posicion]
        
        # Título
        titulo = f"📍 Habitación ({hab.x}, {hab.y})"
        if hab.inicial:
            titulo += " [Entrada]"
        
        # Contenido
        contenido_texto = Text()
        
        if hab.contenido:
            tipo = hab.contenido.tipo
            desc = hab.contenido.descripcion
            
            if tipo == "Jefe Final":
                contenido_texto.append("👑 ", style="bold red")
                contenido_texto.append(f"{tipo}\n", style="bold red")
                contenido_texto.append(f"{desc}", style="red")
            elif tipo == "Monstruo":
                contenido_texto.append("👾 ", style="red")
                contenido_texto.append(f"{tipo}\n", style="bold red")
                contenido_texto.append(f"{desc}", style="red")
            elif tipo == "Cofre del Tesoro":
                contenido_texto.append("💎 ", style="yellow")
                contenido_texto.append(f"{tipo}\n", style="bold yellow")
                contenido_texto.append(f"{desc}", style="yellow")
            elif tipo == "Evento":
                contenido_texto.append("❗ ", style="magenta")
                contenido_texto.append(f"{tipo}\n", style="bold magenta")
                contenido_texto.append(f"{desc}", style="magenta")
        else:
            contenido_texto.append("La habitación está vacía.", style="dim")
        
        # Conexiones
        if hab.conexiones:
            contenido_texto.append("\n\n🚪 Salidas: ", style="bold cyan")
            salidas = ", ".join(hab.conexiones.keys())
            contenido_texto.append(salidas, style="cyan")
        else:
            contenido_texto.append("\n\n🚪 No hay salidas.", style="dim")
        
        panel = Panel(
            contenido_texto,
            title=titulo,
            border_style="cyan"
        )
        self.console.print(panel)
    
    def mostrar_estadisticas_explorador(self, explorador: "Explorador"):
        """Muestra las estadísticas del explorador."""
        texto = Text()
        
        # Vida
        texto.append("❤️  Vida: ", style="bold")
        color_vida = "green" if explorador.vida > 3 else "yellow" if explorador.vida > 1 else "red"
        texto.append(f"{explorador.vida}\n", style=f"bold {color_vida}")
        
        # Daño
        texto.append("⚔️  Daño: ", style="bold")
        texto.append(f"{explorador.dano}\n", style="bold blue")
        
        # Inventario
        texto.append("🎒 Inventario: ", style="bold")
        if explorador.inventario:
            texto.append(f"{len(explorador.inventario)} objetos\n", style="yellow")
            for obj in explorador.inventario:
                texto.append(f"  • {obj.nombre}", style="white")
                texto.append(f" ({obj.valor} oro)\n", style="dim yellow")
        else:
            texto.append("vacío\n", style="dim")
        
        panel = Panel(
            texto,
            title="[bold green]🧙 EXPLORADOR[/bold green]",
            border_style="green"
        )
        self.console.print(panel)
    
    def mostrar_estadisticas_mapa(self):
        """Muestra estadísticas generales del mapa."""
        stats = self.mapa.obtener_estadisticas_mapa()
        
        texto = Text()
        texto.append(f"🏰 Habitaciones: {stats['total_habitaciones']}\n", style="cyan")
        texto.append(f"👾 Monstruos: {stats['monstruos']}\n", style="red")
        texto.append(f"💎 Tesoros: {stats['tesoros']}\n", style="yellow")
        texto.append(f"👑 Jefes: {stats['jefes']}\n", style="bold red")
        texto.append(f"❗ Eventos: {stats['eventos']}\n", style="magenta")
        texto.append(f"·  Vacías: {stats['vacias']}\n", style="dim")
        texto.append(f"🔗 Conexiones promedio: {stats['promedio_conexiones']}", style="blue")
        
        panel = Panel(
            texto,
            title="[bold cyan]📊 ESTADÍSTICAS DEL MAPA[/bold cyan]",
            border_style="cyan"
        )
        self.console.print(panel)
    
    def limpiar_pantalla(self):
        """Limpia la pantalla de la consola."""
        self.console.clear()
    
    def mostrar_mensaje(self, mensaje: str, estilo: str = "white"):
        """Muestra un mensaje con estilo."""
        self.console.print(mensaje, style=estilo)
    
    def mostrar_titulo(self):
        """Muestra el título del juego."""
        titulo = """
        ╔═══════════════════════════════════════╗
        ║                                       ║
        ║      🏰  DUNGEON GENERATOR  🏰        ║
        ║                                       ║
        ║      ¡Explora y conquista!            ║
        ║                                       ║
        ╚═══════════════════════════════════════╝
        """
        self.console.print(titulo, style="bold cyan")
