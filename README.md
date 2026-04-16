# 💀 Clanka

**Clanka** is a terminal-based AI homie built for Linux users who hate bloat and love the CLI. It wraps Google's **Gemma 4** (via Ollama) into a high-end, sarcastic, and context-aware terminal interface.

> "Helpful, but will throw shade if you don't read the man pages."

## 🚀 Features
- **Sexy CLI:** Powered by `rich` for live Markdown streaming and panels.
- **Gemma 4 Native:** Optimized for the `e4b` (Effective 4B) model.
- **Anti-Bloat:** No heavy Electron apps. Just Python and the terminal.
- **Sarcastic Persona:** Custom-tuned to act like a burnt-out sysadmin.

## 🛠️ Installation

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/Vicky404-git/Clanka.git](https://github.com/Vicky404-git/Clanka.git)
   cd Clanka
   ```

2. Setup with uv:
```bash
```
```bash
```
```
uv init
uv add ollama rich
```
```

3. Create the Persona:

Bash
ollama create clanka -f Modelfile

4. Add the Alias:
Add this to your .zshrc or .bashrc:

Bash
alias clanka='uv --directory ~/path/to/Clanka run clanka.py'
## ⌨️ Usage
Bash
clanka "How do I fix my broken I/O?"
## 🛡️ License
Apache 2.0 (Just like Gemma 4). Do whatever you want, clanker.

Built by vicky-404 at 2 AM.
   ```
