import os
import re
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
MAX_FILE_CHARS = int(os.getenv("CLANKA_MAX_CHARS", 4000))

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
# SYSTEM INFO (optional)
# =========================
USE_SYS_CONTEXT = False

def get_sys_info():
    try:
        mem = psutil.virtual_memory()
        return f"{platform.system()} {platform.release()} | {platform.processor()} | {round(mem.total/(1024**3),2)}GB RAM"
    except:
        return "System info unavailable"

# =========================
# STREAM RESPONSE (OPTIMIZED)
# =========================
def stream_response(prompt, quiet=False):
    if not quiet:
        console.print(LOGO)

    if USE_SYS_CONTEXT:
        prompt = f"{get_sys_info()}\n\n{prompt}"

    try:
        stream = ollama.generate(
            model=MODEL_NAME,
            prompt=prompt,
            stream=True
        )

        full = ""
        buffer = ""

        panel = Panel(
            "...",
            title=f"[bold green]{MODEL_NAME}[/bold green]",
            border_style="cyan",
            padding=(1, 2)
        )

        with Live(panel, console=console, refresh_per_second=6) as live:
            for chunk in stream:
                text = chunk.get("response", "")
                if not text:
                    continue

                full += text
                buffer += text

                # 🔥 update less frequently
                if len(buffer) > 120:
                    live.update(Panel(
                        Markdown(full),
                        title=f"[bold green]{MODEL_NAME}[/bold green]",
                        border_style="cyan",
                        padding=(1, 2)
                    ))
                    buffer = ""

            # final render
            live.update(Panel(
                Markdown(full),
                title=f"[bold green]{MODEL_NAME}[/bold green]",
                border_style="cyan",
                padding=(1, 2)
            ))

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")

# =========================
# WTF MODE
# =========================
def handle_wtf(target=None):
    console.print(LOGO)

    if target:
        path = Path(target)

        if not path.exists():
            console.print(f"[red]File not found:[/red] {target}")
            return

        try:
            content = path.read_text(errors="ignore")[:MAX_FILE_CHARS]

            console.print(f"[dim]Analyzing {target}...[/dim]\n")

            prompt = f"""Explain this file:

{content}

Be concise, technical, and highlight issues.
"""

            stream_response(prompt, quiet=True)

        except Exception as e:
            console.print(f"[red]Error:[/red] {e}")

    else:
        cwd = Path.cwd()

        ignore = {'.git', '.venv', 'node_modules', '__pycache__'}
        files = [f.name for f in cwd.iterdir() if not f.name.startswith('.') and f.name not in ignore]

        readme = ""
        if (cwd / "README.md").exists():
            readme = (cwd / "README.md").read_text(errors="ignore")[:800]

        console.print("[dim]Analyzing project...[/dim]\n")

        prompt = f"""Project files:
{", ".join(files[:30])}

README:
{readme}

Explain:
- purpose
- stack
- structure
- issues
"""

        stream_response(prompt, quiet=True)

# =========================
# PATCH MODE
# =========================
def extract_code(text):
    match = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if match:
        return match[0].strip()

    lines = []
    for l in text.splitlines():
        if l.strip().startswith(("#", "//", "`")):
            continue
        lines.append(l)
    return "\n".join(lines).strip()


def handle_patch(target):
    console.print(LOGO)

    path = Path(target)

    if not path.exists():
        console.print(f"[red]File not found:[/red] {target}")
        return

    try:
        content = path.read_text(errors="ignore")[:MAX_FILE_CHARS]

        console.print(f"[dim]Refactoring {target}...[/dim]\n")

        prompt = f"""Return ONLY valid Python code.

Refactor:
{content}
"""

        res = ollama.generate(model=MODEL_NAME, prompt=prompt)
        code = extract_code(res.get("response", ""))

        try:
            compile(code, "<string>", "exec")
        except:
            console.print("[red]Invalid output from model[/red]")
            return

        new_file = path.with_name(f"{path.stem}_fixed{path.suffix}")
        new_file.write_text(code)

        console.print(f"[green]Saved:[/green] {new_file}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
