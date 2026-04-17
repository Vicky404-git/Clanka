import platform
import psutil
import ollama
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel

console = Console()

LOGO = r"""
 [bold cyan]
  ____ _        _    _   _ _  __   _    
 / ___| |      / \  | \ | | |/ /  / \   
| |   | |     / _ \ |  \| | ' /  / _ \  
| |___| |___ / ___ \| |\  | . \ / ___ \ 
 \____|_____/_/   \_\_| \_|_|\_/_/   \_\ [/bold cyan]
 [dim italic]Your Terminal Homie | vicky-404 edition[/dim italic]
"""

def get_sys_info():
    # Gets the specs so Clanka can roast you accurately
    mem = psutil.virtual_memory()
    return f"OS: {platform.system()} {platform.release()}, CPU: {platform.processor()}, RAM: {round(mem.total / (1024**3), 2)}GB"

def stream_response(prompt):
    console.print(LOGO)
    sys_context = get_sys_info()
    enriched_prompt = f"[SYSTEM_CONTEXT: {sys_context}] {prompt}"

    try:
        stream = ollama.generate(model='clanka', prompt=enriched_prompt, stream=True)
        with Live(console=console, refresh_per_second=10, vertical_overflow="visible") as live:
            full_response = ""
            for chunk in stream:
                full_response += chunk['response']
                live.update(Panel(Markdown(full_response), title="[bold green]clanka[/bold green]", border_style="cyan", padding=(1, 2)))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
