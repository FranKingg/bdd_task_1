#!/usr/bin/env python3
"""
Dungeon Generator - Sistema de generación y exploración de dungeons
"""

from dungeon_generator import (
    Mapa, Explorador, Visualizador,
    guardar_partida, cargar_partida,
    generar_reporte_exploracion
)
from rich.console import Console
from rich.prompt import Prompt, IntPrompt, Confirm
import sys


def menu_principal(console: Console):
    """Muestra el menú principal y retorna la opción elegida."""
    console.print("\n[bold cyan]═══════ MENÚ PRINCIPAL ═══════[/bold cyan]")
    console.print("1. 🆕 Nueva partida")
    console.print("2. 💾 Cargar partida")
    console.print("3. 📖 Ver instrucciones")
    console.print("4. 🚪 Salir")
    console.print("[bold cyan]═══════════════════════════════[/bold cyan]")
    
    return Prompt.ask("Elige una opción", choices=["1", "2", "3", "4"], default="1")


def mostrar_instrucciones(console: Console):
    """Muestra las instrucciones del juego."""
    instrucciones = """
    [bold cyan]📖 INSTRUCCIONES[/bold cyan]
    
    [bold yellow]Objetivo:[/bold yellow]
    Explora el dungeon, derrota enemigos, recolecta tesoros y vence al jefe final.
    
    [bold yellow]Comandos de movimiento:[/bold yellow]
    • norte, sur, este, oeste - Moverse en una dirección
    • n, s, e, o - Atajos para movimiento
    
    [bold yellow]Comandos de acción:[/bold yellow]
    • explorar / ex - Interactuar con el contenido de la habitación
    • mapa / m - Ver el mapa completo
    • stats - Ver tus estadísticas
    • inventario / inv - Ver tu inventario
    • ayuda / help - Ver esta ayuda
    • guardar - Guardar la partida actual
    • salir / quit - Salir del juego
    
    [bold yellow]Tipos de contenido:[/bold yellow]
    • 👾 Monstruos - Combate automático, pierdes vida
    • 💎 Tesoros - Objetos valiosos para recolectar
    • 👑 Jefe Final - Batalla épica final
    • ❗ Eventos - Efectos especiales (trampas, curaciones, etc.)
    
    [bold yellow]Consejos:[/bold yellow]
    • Explora cuidadosamente, los monstruos hacen daño
    • Busca tesoros para aumentar tu puntuación
    • El jefe final está en la habitación más lejana
    • Puedes guardar tu progreso en cualquier momento
    
    [bold red]¡Buena suerte, aventurero![/bold red]
    """
    console.print(instrucciones)
    Prompt.ask("\nPresiona Enter para continuar", default="")


def configurar_nueva_partida(console: Console) -> tuple[Mapa, Explorador]:
    """Configura una nueva partida con los parámetros del usuario."""
    console.print("\n[bold cyan]⚙️  CONFIGURACIÓN DE NUEVA PARTIDA[/bold cyan]\n")
    
    # Solicitar tamaño del mapa
    ancho = IntPrompt.ask("Ancho del mapa", default=10)
    alto = IntPrompt.ask("Alto del mapa", default=10)
    
    # Validar tamaño
    if ancho < 3 or alto < 3:
        console.print("[red]El mapa debe ser al menos 3x3[/red]")
        ancho, alto = 10, 10
    
    if ancho > 20 or alto > 20:
        console.print("[yellow]⚠️  Mapa muy grande, limitando a 20x20[/yellow]")
        ancho = min(ancho, 20)
        alto = min(alto, 20)
    
    # Solicitar número de habitaciones
    max_habitaciones = ancho * alto
    n_habitaciones = IntPrompt.ask(
        f"Número de habitaciones (máximo {max_habitaciones})",
        default=min(20, max_habitaciones // 2)
    )
    
    if n_habitaciones < 5:
        console.print("[yellow]Mínimo 5 habitaciones requeridas[/yellow]")
        n_habitaciones = 5
    
    n_habitaciones = min(n_habitaciones, max_habitaciones)
    
    # Crear mapa
    console.print("\n[cyan]🏗️  Generando dungeon...[/cyan]")
    mapa = Mapa(ancho=ancho, alto=alto)
    
    resultado = mapa.generar_estructura(n_habitaciones)
    console.print(f"[green]{resultado}[/green]")
    
    resultado_contenido = mapa.colocar_contenido()
    console.print(f"[green]{resultado_contenido}[/green]")
    
    # Crear explorador
    explorador = Explorador(mapa=mapa)
    if mapa.habitacion_inicial is not None:
        explorador.posicion = (mapa.habitacion_inicial.x, mapa.habitacion_inicial.y)
        mapa.habitacion_inicial.visitada = True
    else:
        console.print("[red]Error: No se pudo inicializar la habitación inicial del mapa.[/red]")
        sys.exit(1)
    
    console.print("\n[bold green]✅ ¡Dungeon creado exitosamente![/bold green]")
    
    # Mostrar estadísticas
    stats = mapa.obtener_estadisticas_mapa()
    console.print(f"\n[cyan]📊 Estadísticas:[/cyan]")
    console.print(f"  • Habitaciones: {stats['total_habitaciones']}")
    console.print(f"  • Monstruos: {stats['monstruos']}")
    console.print(f"  • Tesoros: {stats['tesoros']}")
    console.print(f"  • Jefes: {stats['jefes']}")
    console.print(f"  • Eventos: {stats['eventos']}")
    
    Prompt.ask("\nPresiona Enter para comenzar", default="")
    
    return mapa, explorador


def procesar_comando(comando: str, explorador: Explorador, visualizador: Visualizador, console: Console) -> bool:
    """
    Procesa un comando del jugador.
    Retorna True si el juego debe continuar, False si debe terminar.
    """
    comando = comando.lower().strip()
    
    # Comandos de movimiento
    if comando in ['norte', 'n']:
        if explorador.mover('norte'):
            console.print("[green]Te mueves hacia el norte.[/green]")
            visualizador.mostrar_habitacion_actual(explorador)
        else:
            console.print("[red]No puedes ir en esa dirección.[/red]")
    
    elif comando in ['sur', 's']:
        if explorador.mover('sur'):
            console.print("[green]Te mueves hacia el sur.[/green]")
            visualizador.mostrar_habitacion_actual(explorador)
        else:
            console.print("[red]No puedes ir en esa dirección.[/red]")
    
    elif comando in ['este', 'e']:
        if explorador.mover('este'):
            console.print("[green]Te mueves hacia el este.[/green]")
            visualizador.mostrar_habitacion_actual(explorador)
        else:
            console.print("[red]No puedes ir en esa dirección.[/red]")
    
    elif comando in ['oeste', 'o']:
        if explorador.mover('oeste'):
            console.print("[green]Te mueves hacia el oeste.[/green]")
            visualizador.mostrar_habitacion_actual(explorador)
        else:
            console.print("[red]No puedes ir en esa dirección.[/red]")
    
    # Comandos de acción
    elif comando in ['explorar', 'ex']:
        resultado = explorador.explorar_habitacion()
        console.print(f"\n{resultado}\n")
        
        if not explorador.esta_vivo:
            console.print("[bold red]💀 HAS MUERTO 💀[/bold red]")
            console.print(generar_reporte_exploracion(explorador))
            return False
    
    elif comando in ['mapa', 'm']:
        visualizador.mostrar_mapa_completo(explorador)
    
    elif comando == 'stats':
        visualizador.mostrar_estadisticas_explorador(explorador)
    
    elif comando in ['inventario', 'inv']:
        if explorador.inventario:
            console.print("\n[bold yellow]🎒 INVENTARIO:[/bold yellow]")
            for i, obj in enumerate(explorador.inventario, 1):
                console.print(f"  {i}. [cyan]{obj.nombre}[/cyan] - {obj.descripcion} ([yellow]{obj.valor} oro[/yellow])")
            
            from dungeon_generator.utils import calcular_valor_total_inventario
            total = calcular_valor_total_inventario(explorador)
            console.print(f"\n[bold yellow]💰 Valor total: {total} oro[/bold yellow]")
        else:
            console.print("[dim]Tu inventario está vacío.[/dim]")
    
    elif comando in ['ayuda', 'help']:
        mostrar_instrucciones(console)
    
    elif comando == 'guardar':
        resultado = guardar_partida(explorador)
        console.print(f"[green]{resultado}[/green]")
    
    elif comando in ['salir', 'quit']:
        if Confirm.ask("¿Deseas guardar antes de salir?"):
            guardar_partida(explorador)
            console.print("[green]Partida guardada.[/green]")
        console.print("[cyan]¡Hasta pronto, aventurero![/cyan]")
        return False
    
    else:
        console.print(f"[red]Comando desconocido: '{comando}'. Escribe 'ayuda' para ver los comandos.[/red]")
    
    return True


def bucle_juego(explorador: Explorador, visualizador: Visualizador, console: Console):
    """Bucle principal del juego."""
    visualizador.limpiar_pantalla()
    visualizador.mostrar_titulo()
    
    console.print("\n[bold green]¡Bienvenido al dungeon![/bold green]")
    console.print("[dim]Escribe 'ayuda' para ver los comandos disponibles.[/dim]\n")
    
    visualizador.mostrar_habitacion_actual(explorador)
    visualizador.mostrar_estadisticas_explorador(explorador)
    
    while explorador.esta_vivo:
        comando = Prompt.ask("\n[bold cyan]¿Qué deseas hacer?[/bold cyan]")
        
        if not procesar_comando(comando, explorador, visualizador, console):
            break
        
        # Verificar victoria
        hay_jefe = False
        for hab in explorador.mapa.habitaciones.values():
            if hab.contenido and hab.contenido.tipo == "Jefe Final":
                hay_jefe = True
                break
        
        if not hay_jefe and explorador.esta_vivo:
            console.print("\n" + "=" * 60)
            console.print("[bold yellow]🎉 ¡FELICIDADES! ¡HAS COMPLETADO EL DUNGEON! 🎉[/bold yellow]")
            console.print("=" * 60)
            console.print(generar_reporte_exploracion(explorador))
            break


def main():
    """Función principal del juego."""
    console = Console()
    
    while True:
        opcion = menu_principal(console)
        
        if opcion == "1":  # Nueva partida
            mapa, explorador = configurar_nueva_partida(console)
            visualizador = Visualizador(mapa)
            bucle_juego(explorador, visualizador, console)
        
        elif opcion == "2":  # Cargar partida
            console.print("\n[cyan]📂 Cargando partida...[/cyan]")
            explorador = cargar_partida()
            
            if explorador:
                console.print("[green]✅ Partida cargada exitosamente.[/green]")
                visualizador = Visualizador(explorador.mapa)
                bucle_juego(explorador, visualizador, console)
            else:
                console.print("[red]❌ No se encontró ninguna partida guardada.[/red]")
                Prompt.ask("Presiona Enter para continuar", default="")
        
        elif opcion == "3":  # Instrucciones
            mostrar_instrucciones(console)
        
        elif opcion == "4":  # Salir
            console.print("\n[cyan]👋 ¡Gracias por jugar! ¡Hasta pronto![/cyan]")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console = Console()
        console.print("\n\n[yellow]⚠️  Juego interrumpido por el usuario.[/yellow]")
        sys.exit(0)
    except Exception as e:
        console = Console()
        console.print(f"\n[bold red]❌ Error inesperado: {e}[/bold red]")
        import traceback
        console.print(traceback.format_exc())
        sys.exit(1)
