import os
import platform
import psutil
import ollama
from pathlib import Path
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel

console = Console()
MODEL_NAME = os.getenv("CLANKA_MODEL", "clanka")
MAX_FILE_CHARS = 4000
LOGO = r"""
 [bold cyan]
  ____ _        _    _   _ _  __   _    
 / ___| |      / \  | \ | | |/ /  / \   
| |   | |     / _ \ |  \| | ' /  / _ \  
| |___| |___ / ___ \| |\  | . \ / ___ \ 
 \____|_____/_/   \_\_| \_|_|\_/_/   \_\ [/bold cyan]
 [dim italic]Your Terminal Homie | vicky-404 edition[/dim italic]
"""

# =========================
# SYSTEM INFO
# =========================
def get_sys_info():
    try:
        mem = psutil.virtual_memory()
        return f"OS: {platform.system()} {platform.release()}, CPU: {platform.processor()}, RAM: {round(mem.total / (1024**3), 2)}GB"
    except Exception:
        return "System info unavailable"

# =========================
# STREAM RESPONSE
# =========================
def stream_response(prompt, quiet=False):
    if not quiet:
        console.print(LOGO)

    sys_context = get_sys_info()
    enriched_prompt = f"""SYSTEM CONTEXT:
{sys_context}

USER:
{prompt}
"""

    try:
        stream = ollama.generate(
            model=MODEL_NAME,
            prompt=enriched_prompt,
            stream=True
        )

        initial_panel = Panel(
            Markdown("..."),
            title=f"[bold green]{MODEL_NAME}[/bold green]",
            border_style="cyan",
            padding=(1, 2)
        )

        with Live(initial_panel, console=console, refresh_per_second=8) as live:
            full_response = ""

            for chunk in stream:
                if "response" not in chunk:
                    continue  # safety

                full_response += chunk["response"]

                live.update(
                    Panel(
                        Markdown(full_response),
                        title=f"[bold green]{MODEL_NAME}[/bold green]",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                )

    except ollama.ResponseError as e:
        console.print(f"[bold red]Ollama API Error:[/bold red] {e}")
    except Exception as e:
        console.print(f"[bold red]Unexpected Error:[/bold red] {e}")
# =========================
# WTF MODE
# =========================
def handle_wtf(target=None):
    console.print(LOGO)

    # FILE MODE
    if target:
        file_path = Path(target)

        if file_path.is_file():
            try:
                content = file_path.read_text(errors='ignore')[:MAX_FILE_CHARS]

                console.print(f"[dim]Analyzing file: {target}...[/dim]\n")

                prompt = f"""Read this file ({target}) and explain what it does.
                Be concise, technical, and point out issues or bad patterns.

                File Content:{content}"""

                stream_response(prompt, quiet=True)

            except FileNotFoundError:
                console.print(f"[bold red]File not found:[/bold red] {target}")
            except PermissionError:
                console.print(f"[bold red]Permission denied:[/bold red] {target}")
            except Exception as e:
                console.print(f"[bold red]Error reading file:[/bold red] {e}")

        else:
            console.print(f"[bold red]Error:[/bold red] File '{target}' not found.")

    # DIRECTORY MODE
    else:
        try:
            cwd = Path.cwd()
            
            # Filter out hidden files/folders and massive dependency directories
            ignore_dirs = {'.git', '.venv', 'node_modules', '__pycache__', '.idea'}
            valid_files = []
            for f in cwd.iterdir():
                try:
                    if f.name not in ignore_dirs and not f.name.startswith('.'):
                        valid_files.append(f.name)
                except PermissionError:
                    continue 
            
            # Limit to top 30 files to protect the context window
            files_str = ", ".join(valid_files[:30])[:1000]
            if len(valid_files) > 30:
                files_str += f"... and {len(valid_files) - 30} more."

            readme_content = ""
            readme_path = cwd / "README.md"

            if readme_path.exists():
                readme_content = readme_path.read_text(errors='ignore')[:800]

            console.print("[dim]Analyzing current directory...[/dim]\n")

            prompt = f"""You're analyzing a project.

Files:
{files_str}

README preview:
{readme_content}

Explain:
- What this project does
- Tech stack
- Structure
- Issues / missing parts
"""

            stream_response(prompt, quiet=True)

        except Exception as e:
            console.print(f"[bold red]Error reading directory:[/bold red] {e}")
