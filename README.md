# ⚡ Clanka

> Terminal-native AI assistant with local inference, clean TUI, and evolving RAG

Clanka is a fast, offline-first CLI tool for interacting with local LLMs using Ollama — built for developers who prefer terminal workflows over bloated GUIs.

---

## 🚀 What is Clanka?

Clanka is:

* 🧠 a **local AI assistant**
* ⚡ a **low-latency CLI interface**
* 📂 a **code-aware analyzer**
* 🎨 a **terminal-native UI experiment (but actually usable)**

Clanka is NOT:

* ❌ cloud-dependent
* ❌ a heavy framework
* ❌ an IDE replacement

---

## ⚡ Features

### 💬 Chat with Local Models

```bash
clanka "explain this code"
```

* Runs fully local (via Ollama)
* No API keys
* Streaming responses

---

### 📂 File / Project Awareness

```bash
clanka wtf file.py
clanka wtf
```

* Reads files directly
* Understands directory structure
* Uses README context when available

---

### 🛠 Patch Mode (Safe Refactor)

```bash
clanka patch file.py
```

* Refactors code using AI
* **Never overwrites original file**
* Creates: `file_fixed.py`

---

### 🎨 Terminal UI

* Built with `rich`
* Markdown rendering
* Live streaming panels
* Optimized updates (less flicker, less CPU waste)

---

### 🧪 Debug Mode

```bash
clanka debug
```

Checks:

* Python version
* Dependencies
* Ollama daemon
* Model availability
* Inference working
* File system permissions

---

## ⚙️ Tech Stack

* Python
* Ollama
* Local LLMs (Gemma etc.)
* rich (TUI)
* psutil

---

## 📦 Installation

```bash
git clone https://github.com/Vicky404-git/Clanka.git
cd Clanka
pip install -e .
```

---

## 🧠 Model Setup

```bash
ollama create clanka -f Modelfile
ollama list
```

---

## ▶️ Usage

```bash
clanka "your prompt"
clanka wtf file.py
clanka wtf
clanka patch file.py
clanka debug
```

---

## 📁 Project Structure

```
core/
  ├── clanka.py     # core engine + UI
  ├── debug.py      # diagnostics

memory/
  └── clanka_memory.json  # (future RAG storage)

main.py             # CLI entrypoint
Modelfile           # model config
```

---

## ⚠️ Performance Note

If upgrading from older versions:

```bash
ollama rm gemma4:e4b
ollama rm clanka
ollama create clanka -f Modelfile
```

Prevents stale model weights slowing down inference.

---

## 🔮 Roadmap

* Persistent memory (RAG)
* Multi-persona system (linux / coding / AI / trading)
* Better context chunking
* Faster streaming modes

---

## 👤 Author

Vicky404
https://github.com/Vicky404-git

---

## 🧠 Philosophy

Clanka focuses on:

* local-first AI
* minimal dependencies
* terminal workflows
* fast iteration

---

## 🧨 Note

Clanka is evolving.

Not perfect yet — but getting fast, usable, and actually practical.
