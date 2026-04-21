import os
import sys
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



# =========================
# FIX MODE
# =========================

#def handle_fix(target=None):
#    console.print(LOGO)
#
#    try:
        # =========================
        # 📄 FILE INPUT
        # =========================
#        if target:
#            file_path = Path(target)
#
#            if not file_path.exists():
#                console.print(f"[bold red]Error:[/bold red] File not found: {target}")
#                return
#
#            error_content = file_path.read_text(errors="ignore")[:MAX_FILE_CHARS]

        # =========================
        # 🔌 PIPE INPUT
        # =========================
#        else:
#            if not os.isatty(0):
#                error_content = sys.stdin.read()[:MAX_FILE_CHARS]
#            else:
#                console.print("[bold red]No input provided.[/bold red]")
#                return

        # =========================
        # 🧠 LOCAL ERROR CHECKS (NEW)
        # =========================

#        if not error_content.strip():
#            console.print("[bold red]No error content detected.[/bold red]")
#            return

        # 🚨 Case 1: File not found
#        if "No such file or directory" in error_content:
#            console.print("[bold red]File not found error detected.[/bold red]")
#            console.print("[yellow]Fix:[/yellow] Check filename or path using `ls`")
#            return

        # 🚨 Case 2: Module not found
#        if "ModuleNotFoundError" in error_content:
#            console.print("[bold red]Missing Python module detected.[/bold red]")
#            console.print("[yellow]Fix:[/yellow] Install using `pip install <module>`")
#            return

        # 🚨 Case 3: Syntax error
#        if "SyntaxError" in error_content:
#            console.print("[bold red]Syntax error detected.[/bold red]")
#            console.print("[yellow]Fix:[/yellow] Check your code formatting or indentation")
#            return

        # =========================
        # 🤖 FALLBACK TO AI
        # =========================
#       console.print("[dim]Analyzing error with AI...[/dim]\n")
#
#        prompt = f"""You are an expert debugger.
#
#Analyze this error:
#
#{error_content}

#Return:
#- Explanation
#- Root cause
#- Fix
#"""
#
#        stream_response(prompt, quiet=True)
#
#    except Exception as e:
#       console.print(f"[bold red]Unexpected failure:[/bold red] {e}")
#



# =========================
# PATCH MODE
# =========================

def extract_code(text: str) -> str:
    

    # Prefer fenced code blocks
    matches = re.findall(r"```(?:python)?\n(.*?)```", text, re.DOTALL)
    if matches:
        return matches[0].strip()

    # Remove markdown artifacts
    text = re.sub(r"^```.*?\n", "", text, flags=re.MULTILINE)
    text = text.replace("```", "")

    # Remove obvious non-code lines (very important)
    lines = text.splitlines()
    cleaned = []

    for line in lines:
        if line.strip().startswith(("#", "//", "[", "`")):
            continue
        cleaned.append(line)

    return "\n".join(cleaned).strip()


def handle_patch(target):
    console.print(LOGO)

    path = Path(target)

    if not path.exists():
        console.print(f"[bold red]File not found:[/bold red] {target}")
        return

    def generate_code(prompt):
        response = ""
        stream = ollama.generate(model=MODEL_NAME, prompt=prompt, stream=True)
        for chunk in stream:
            response += chunk.get("response", "")
        return response

    try:
        content = path.read_text(errors="ignore")[:MAX_FILE_CHARS]

        console.print(f"[dim]Generating improved version of {target}...[/dim]\n")

        prompt = f"""You are a senior Python engineer.

Refactor the following code.

STRICT RULES:
- Output ONLY valid Python code
- No explanations
- No markdown
- No backticks

Code:
{content}
"""

        # 🔁 First attempt
        response = generate_code(prompt)
        clean_code = extract_code(response)

        try:
            compile(clean_code, "<string>", "exec")

        except SyntaxError:
            console.print("[yellow]Retrying with stricter prompt...[/yellow]")

            strict_prompt = f"""Return ONLY valid Python code.

NO text.
NO explanation.
ONLY code.

Code:
{content}
"""

            response = generate_code(strict_prompt)
            clean_code = extract_code(response)

            try:
                compile(clean_code, "<string>", "exec")
            except SyntaxError as e:
                console.print("[bold red]Failed again. Model output unusable.[/bold red]")
                console.print(f"[dim]{e}[/dim]")
                return

        # ✅ SAVE AFTER VALIDATION
        new_file = path.with_name(f"{path.stem}_fixed{path.suffix}")
        new_file.write_text(clean_code)

        console.print(f"[bold green]Saved fixed version:[/bold green] {new_file}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")


