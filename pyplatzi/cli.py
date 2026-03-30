import logging
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from pyplatzi import PlatziClient, __version__

logging.basicConfig(
    level="INFO",
    format="%(message)s", 
    datefmt="[%X]",
    handlers=[
        RichHandler(
            rich_tracebacks=True, 
            show_path=False,    
            show_time=True,     
            markup=True
        )
    ]
)

logger = logging.getLogger("pyplatzi")

app = typer.Typer(
    help="CLI para interactuar con la API de Platzi",
    no_args_is_help=True,
    add_completion=False
)
console = Console()

def version_callback(value: bool):
    if value:
        console.print(f"[bold cyan]pyplatzi v{__version__}[/bold cyan]")
        raise typer.Exit()


@app.callback()
def main(version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        callback=version_callback,
        is_eager=True,
        help="Muestra la versión de la aplicación.",
    ),):
    """
    Herramienta CLI para interactuar con la API de Platzi.
    Usa los subcomandos disponibles para realizar acciones.
    """
    pass

@app.command(name="my-courses")
def get_my_courses(
    cookies_path: Path = typer.Option(
        "platzi.com_cookies.txt", 
        "--cookies", "-c", 
        help="Ruta al archivo de cookies (.txt format Mozilla)"
    ),
    output: Optional[Path] = typer.Option(
        None, 
        "--output", "-o", 
        help="Ruta opcional para guardar el resultado en formato JSON"
    ),
):
    """
    Obtiene la lista de cursos aprobados y los muestra en consola o los guarda en un JSON.
    """
    try:
        if not cookies_path.exists():
            console.print(f"[bold red]Error:[/bold red] El archivo de cookies no existe en: {cookies_path}")
            raise typer.Exit(code=1)

        with console.status("[bold green]Consultando cursos en Platzi..."):
            client = PlatziClient(cookies_path=cookies_path)
            data = client.get_all_approved_courses()

        if not data.courses:
            console.print("[yellow]No se encontraron cursos aprobados.[/yellow]")
            return

        if output:
            output.parent.mkdir(parents=True, exist_ok=True)
            if output.suffix=="":                output = output / f"{output.name}.json"
                
            output.write_text(data.model_dump_json(indent=4), encoding="utf-8")
            console.print(f"[bold green]✔[/bold green] Se han exportado {len(data.courses)} cursos a: [cyan]{output}[/cyan]")
        else:
            table = Table(title=f"Mis Cursos Aprobados ({data.approved_courses} en total)")
            
            table.add_column("ID", justify="right", style="cyan", no_wrap=True)
            table.add_column("Título", style="white")
            table.add_column("Fecha de Aprobación", style="green")
            table.add_column("Progreso", justify="center", style="magenta")

            for course in data.courses:
                table.add_row(
                    str(course.id),
                    course.title,
                    course.diploma.approved_date,
                    f"{course.progress}%"
                )

            console.print(table)

    except Exception as e:
        console.print(f"[bold red]Ocurrió un error inesperado:[/bold red] {e}")
        raise typer.Exit(code=1)

def run_script():
    app()

if __name__ == "__main__":
    app()