# ⚡ Clanka — Your Terminal Debugging Engine

> Not a chatbot. Not a notes app.
> **Clanka is a developer reflex system.**

Clanka is a **terminal-native AI assistant** built for developers who want fast, local, no-BS debugging and code analysis.

It reads your code.
It understands your system.
It fixes your mistakes.

---

## 🚀 Core Idea

Most AI tools sit in a browser.

Clanka lives where you actually work:

> **your terminal**

It turns your CLI into a:

* code analyzer
* debugger
* refactoring engine
* real-time AI assistant

---

## ⚡ Features

### 🔍 `wtf` — Code & Project Analysis

```bash
clanka wtf script.py
clanka wtf
```

* Explains code
* Finds bugs & bad patterns
* Analyzes full project structure
* Reads README + files for context

---

### 🛠 `patch` — Safe Refactoring

```bash
clanka patch script.py
```

* Generates improved version
* Saves as `*_fixed.py`
* Never overwrites original file
* Ensures valid Python output

---

### 🧠 `debug` — Preflight Diagnostics

```bash
clanka debug
```

Checks your environment:

* Python version
* Dependencies
* Ollama status
* Model availability
* Inference speed
* File system permissions
* CLI availability

---

### 💬 Direct AI Mode

```bash
clanka "optimize this logic"
```

* Streams response in real-time
* Markdown-rendered output
* System-aware responses (CPU, RAM, OS)

---

## ⚙️ Tech Stack

* **Python**
* **Ollama** (local LLM)
* **rich** (terminal UI)
* **psutil** (system awareness)
* **pathlib / os** (file handling)

---

## 🧠 How It Works

Clanka injects **system context** into every prompt:

* OS
* CPU
* RAM

Then combines it with:

* your code
* your files
* your command

Result:

> grounded, context-aware responses

---

## 🏗 Project Structure

```
clanka.py      → core engine (AI + logic)
main.py        → CLI router
debug.py       → environment diagnostics
Modelfile      → Ollama model config
README.md      → docs
```

---

## 🛠 Installation

### 1. Clone repo

```bash
git clone https://github.com/Vicky404-git/Clanka.git
cd Clanka
```

### 2. Install dependencies

```bash
pip install -e .
```

### 3. Setup Ollama

```bash
ollama create clanka -f Modelfile
```

---

## ▶️ Usage

```bash
clanka wtf file.py
clanka patch file.py
clanka debug
clanka "explain this error"
```

---

## ⚠️ Philosophy

Clanka is **not**:

* a notes app
* a knowledge system
* a life tracker

That’s what Sōzō is for.

---

Clanka is:

> ⚡ fast
> ⚡ local
> ⚡ brutal
> ⚡ developer-first

---

## 🧨 Design Principles

* No GUI bloat
* No cloud dependency
* No silent file overwrites
* Always show what changed
* Fail fast, explain clearly

---

## 🔥 Roadmap

* `reflex` → run + debug in one command
* multi-file patching
* smarter error detection (no AI needed)
* faster inference mode
* plugin system

---

## 👤 Author

**Vicky404**

GitHub: https://github.com/Vicky404-git

---

## 💀 Final Note

Clanka doesn’t try to be friendly.

It tries to be:

> **useful.**

