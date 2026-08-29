# ⚡ Clanka

> Terminal-native AI assistant with local inference, resource-aware throttling, and persistent memory (RAG)

Clanka is a fast, offline-first CLI tool for interacting with local LLMs using Ollama — built for developers who prefer terminal workflows over bloated GUIs.

---

## 🚀 What is Clanka?

Clanka is:

* 🧠 a **local AI assistant**
* ⚡ a **low-latency CLI interface**
* 📂 a **code-aware analyzer**
* 🧵 a **resource-aware assistant** (you set the % of system resources it's allowed to use)
* 💾 a **persistent-memory assistant** (remembers past conversations across sessions)
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
* Automatically pulls relevant context from memory (past chats + indexed code/docs)

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

### 🧵 Resource Control

```bash
clanka config --mem 30    # cap Clanka at ~30% of system resources
clanka config              # view current config
```

* One knob (`mem_percent`, default 50) controls context window size, thread count, and how much memory context gets pulled per query
* Fixes the "5-10 min wait while your PC lags" problem — lower it when multitasking, raise it when Clanka has the machine to itself
* Persists to `~/.clanka/config.json`

---

### 💾 Persistent Memory (RAG)

```bash
clanka index .        # (re)build the code/doc index
```

* Backed by `sqlite-vec` for fast local vector search
* Three kinds of memory, tracked separately:
  * `code` — your project's source files
  * `doc` — manuals/README/markdown docs
  * `chat` — conversation history, written automatically after every exchange
* Rebuilding the index (`clanka index`) refreshes `code`/`doc` **without ever touching `chat` memory** — your conversation history survives project re-indexing

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
* `sqlite-vec` (vector search)
* `rich` (TUI)
* `psutil`

---

## 📦 Installation

```bash
git clone https://github.com/Vicky404-git/Clanka.git
cd Clanka
uv sync
```

---

## 🧠 Model Setup

```bash
ollama create clanka -f Modelfile
ollama list
ollama pull nomic-embed-text   # required for RAG/embeddings
```

---

## ▶️ Usage

```bash
clanka "your prompt"
clanka wtf file.py
clanka wtf
clanka patch file.py
clanka index .
clanka config
clanka config --mem 30
clanka debug
```

---

## 📁 Project Structure

```
core/
  ├── clanka.py     # core engine + UI (chat, wtf, patch)
  ├── config.py     # resource control (mem_percent -> Ollama/RAG params)
  ├── rag.py        # sqlite-vec RAG engine (code/doc/chat memory)
  └── debug.py      # pre-flight diagnostics

memory/
  └── clanka.db     # local vector store (gitignored, regenerate with `clanka index`)

main.py             # CLI entrypoint
Modelfile           # model config
```

---

## ⚠️ Performance Note

If upgrading from older versions:

```bash
rm -rf memory/                          # old schema is incompatible, will error
ollama rm gemma4:e4b
ollama rm clanka
ollama create clanka -f Modelfile
```

If inference fails with a "requires more system memory than is available" error, lower your resource budget:

```bash
clanka config --mem 20
```

---

## 🔮 Roadmap

* ✅ Persistent memory (RAG)
* ✅ Resource control (`mem_percent`)
* Multi-persona system (linux / coding / AI / trading)
* Weekly memory consolidation (importance scoring + summarization, atomic file swap)
* DaemonV integration (offline, decoupled core)
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
* respecting your machine's resources

---

## 🧨 Note

Clanka is evolving.

Not perfect yet — but getting fast, usable, and actually practical.
