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

from core import rag
from core import config as cfg

console = Console()
MODEL_NAME = os.getenv("CLANKA_MODEL", "clanka")

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
    except Exception:
        return "System info unavailable"


def _build_memory_context(prompt, source_types=None):
    """Pulls relevant chunks from RAG and formats them as prompt context.
    Returns "" if nothing relevant or RAG isn't available yet (no DB, no embed model).
    """
    rag_params = cfg.get_rag_params()
    results = rag.search(prompt, top_k=rag_params["top_k"], source_types=source_types)
    if not results:
        return ""

    lines = ["Relevant context from memory:"]
    for _, doc in results:
        snippet = doc["content"][: rag_params["max_file_chars"] // max(len(results), 1)]
        lines.append(f"- ({doc['source_type']}) {doc['file']}: {snippet}")
    return "\n".join(lines) + "\n\n"


# =========================
# STREAM RESPONSE (OPTIMIZED)
# =========================
def stream_response(prompt, quiet=False, persona=None):
    if not quiet:
        console.print(LOGO)

    options = cfg.get_ollama_options()
    memory_context = _build_memory_context(prompt)

    full_prompt = prompt
    if USE_SYS_CONTEXT:
        full_prompt = f"{get_sys_info()}\n\n{full_prompt}"
    if memory_context:
        full_prompt = f"{memory_context}{full_prompt}"

    try:
        stream = ollama.generate(
            model=MODEL_NAME,
            prompt=full_prompt,
            stream=True,
            options=options,
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

                if len(buffer) > 120:
                    live.update(Panel(
                        Markdown(full),
                        title=f"[bold green]{MODEL_NAME}[/bold green]",
                        border_style="cyan",
                        padding=(1, 2)
                    ))
                    buffer = ""

            live.update(Panel(
                Markdown(full),
                title=f"[bold green]{MODEL_NAME}[/bold green]",
                border_style="cyan",
                padding=(1, 2)
            ))

        # write path: store this exchange as chat memory (fire-and-forget-ish;
        # a failed embed just returns None, doesn't break the chat)
        rag.add_chat_memory(prompt, full, persona=persona)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


# =========================
# WTF MODE
# =========================
def handle_wtf(target=None):
    console.print(LOGO)
    rag_params = cfg.get_rag_params()
    max_chars = rag_params["max_file_chars"]

    if target:
        path = Path(target)

        if not path.exists():
            console.print(f"[red]File not found:[/red] {target}")
            return

        try:
            content = path.read_text(errors="ignore")[:max_chars]

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
    rag_params = cfg.get_rag_params()
    max_chars = rag_params["max_file_chars"]

    path = Path(target)

    if not path.exists():
        console.print(f"[red]File not found:[/red] {target}")
        return

    try:
        content = path.read_text(errors="ignore")[:max_chars]

        console.print(f"[dim]Refactoring {target}...[/dim]\n")

        prompt = f"""Return ONLY valid Python code.

Refactor:
{content}
"""

        options = cfg.get_ollama_options()
        res = ollama.generate(model=MODEL_NAME, prompt=prompt, options=options)
        code = extract_code(res.get("response", ""))

        try:
            compile(code, "<string>", "exec")
        except Exception:
            console.print("[red]Invalid output from model[/red]")
            return

        new_file = path.with_name(f"{path.stem}_fixed{path.suffix}")
        new_file.write_text(code)

        console.print(f"[green]Saved:[/green] {new_file}")

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
