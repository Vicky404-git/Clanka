import sys
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

def stream_response(prompt):
    console.print(LOGO)
    console.print(f"[bold purple]vicky-404[/bold purple] [bold white][/bold white] {prompt}\n")

    try:
        # Initializing the stream from Ollama
        stream = ollama.generate(
            model='clanka',
            prompt=prompt,
            stream=True,
        )

        with Live(console=console, refresh_per_second=10) as live:
            full_response = ""
            for chunk in stream:
                text = chunk['response']
                full_response += text
                
                # Render the accumulated text as Markdown
                live.update(
                    Panel(
                        Markdown(full_response),
                        title="[bold green]clanka[/bold green]",
                        border_style="cyan",
                        padding=(1, 2)
                    )
                )
    except Exception as e:
        console.print(f"[bold red]ERROR:[/bold red] Is Ollama running? {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        stream_response(user_input)
    else:
        console.print("[yellow]Usage:[/yellow] clanka 'Your message here'")
