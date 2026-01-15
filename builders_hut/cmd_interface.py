from pathlib import Path

import typer
from rich.console import Console

from builders_hut.setups import (
    SetupEnv,
    SetupFiles,
    SetupFileWriter,
    SetupStructure,
)
from builders_hut.utils import setup_project

console = Console()
app = typer.Typer(invoke_without_command=True)

BANNER = r"""
[bold cyan]
 ____        _ _     _                 _   _       _   
| __ ) _   _(_) | __| | ___ _ __ ___  | | | |_   _| |_ 
|  _ \| | | | | |/ _` |/ _ \ '__/ __| | |_| | | | | __|
| |_) | |_| | | | (_| |  __/ |  \__ \ |  _  | |_| | |_ 
|____/ \__,_|_|_|\__,_|\___|_|  |___/ |_| |_|\__,_|\__|
[/bold cyan]
[dim]🏠 FastAPI Scaffolding Tool[/dim]
"""


@app.callback()
def main():
    """Builders Hut – FastAPI Scaffolding Tool"""
    console.print(BANNER)


@app.command()
def build(
    name: str = typer.Option(
        None,
        "--name",
        "-n",
        help="Project name",
        prompt="Enter project title",
    ),
    description: str = typer.Option(
        "A new project",
        "--description",
        "-d",
        help="Project description",
        prompt="Enter project description",
    ),
    version: str = typer.Option(
        "0.1.0",
        "--version",
        "-v",
        help="Project version",
        prompt="Enter project version",
    ),
    path: Path = typer.Option(
        Path.cwd() / "demo",
        "--path",
        "-p",
        help="Project directory",
    ),
):
    """
    Build project structure (CLI or interactive).
    """
    try:
        project_location = path.resolve()

        if project_location.exists():
            typer.secho(
                f"Directory already exists: {project_location}",
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)

        setup_steps = [
            SetupStructure,
            SetupFiles,
            SetupEnv,
            SetupFileWriter,
        ]

        for setup in setup_steps:
            setup_project(
                project_location,
                setup,
                name=name,
                description=description,
                version=version,
            )

        typer.secho(
            "Project setup completed successfully.",
            fg=typer.colors.GREEN,
        )

    except Exception as e:
        typer.secho(
            f"Project setup failed: {e}",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=1)


@app.command()
def add():
    """Add components to an existing project."""
    console.print("[yellow]Add command not implemented yet[/yellow]")
