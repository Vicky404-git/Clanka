# 💀 Clanka

**Clanka** is a terminal-native AI assistant built for developers who live in the CLI and hate bloated GUIs.
It runs locally using **Ollama** and streams responses in real-time with a clean `rich` interface.

> Helpful. Fast. Slightly disrespectful.

---

## ⚡ Features

### 🧠 Local AI (No Cloud Dependency)

* Runs entirely on your machine using Ollama
* Uses a custom `clanka` persona model

### 🎨 Rich Terminal UI

* Live streaming responses (no waiting for full output)
* Markdown rendering (code blocks, formatting)
* Clean panel-based interface

### 🔍 `wtf` Mode (Codebase Analyzer)

* `clanka wtf file.py` → Explains + critiques code
* `clanka wtf` → Analyzes entire project structure
* Detects patterns, issues, and skill level

### 🖥️ System Awareness

* Injects system info (CPU, RAM, OS) into every prompt
* Gives context-aware responses

### 🧪 Pre-flight Diagnostics

Run:

```bash
python debug.py
```

Checks:

* Python version
* Dependencies
* Ollama daemon
* Model availability
* Inference test

---

## 🛠️ Installation

### 1. Clone the Repo

```bash
git clone https://github.com/Vicky404-git/Clanka.git
cd Clanka
```

### 2. Setup Environment (Recommended: uv)

```bash
uv sync
```

If you don’t use `uv`:

```bash
pip install ollama rich psutil
```

---

### 3. Create the Model

```bash
ollama create clanka -f Modelfile
```

Verify:

```bash
ollama list
```

---

### 4. Run Diagnostics (Optional but Smart)

```bash
python debug.py
```

You should see:

```
[SUCCESS] ALL SYSTEMS GO
```

---

### 5. Add CLI Command

Add this to your `.zshrc` or `.bashrc`:

```bash
alias clanka="uv run main.py"
```

Somewhere script_fixedbetween productivity and burnout.

---

## 🧠 Future Ideas

* `clanka fix error.log` (auto-debugging)
* Git-aware summaries (`git diff` analysis)
* Multi-file dependency mapping
* Plugin system

---

> If it breaks, Clanka will tell you. Rudely.

