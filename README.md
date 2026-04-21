# 🧪 Clanka

> A terminal playground for experimenting with local AI (Ollama + Gemma)

Clanka is a lightweight CLI tool for interacting with local language models directly from your terminal.
It’s built for fast experimentation, not production workflows.

---

## ⚡ What is Clanka?

Clanka is:

* a **local AI sandbox**
* a **file-aware prompt runner**
* a **terminal UI experiment**

Clanka is NOT:

* a full developer tool
* a polished product
* a replacement for IDEs

---

## 🚀 Features

### 💬 Chat with Local Models

```bash
clanka "explain this code"
```

* Runs locally via Ollama
* Streams responses in real-time
* No API keys, no cloud

---

### 📂 File-Aware AI

```bash
clanka wtf script.py
clanka wtf
```

* Reads files from your system
* Understands project structure
* Uses README + file context

---

### 🎨 Terminal UI

* Built with `rich`
* Live streaming output
* Markdown rendering
* Clean panel-based display

---

### 🧠 System Context Injection

Clanka automatically includes:

* OS
* CPU
* RAM

So responses are grounded in your environment.

---

### 🧪 Debug Mode

```bash
clanka debug
```

Checks:

* Python version
* Dependencies
* Ollama status
* Model availability
* Inference working
* File system access

---

## ⚙️ Tech Stack

* Python
* Ollama
* Gemma (or any local model)
* rich
* psutil

---

## 🛠 Installation

```bash
git clone https://github.com/Vicky404-git/Clanka.git
cd Clanka
pip install -e .
```

---

## 🧠 Setup Model

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
clanka debug
```

---

## 📁 Structure

```
clanka.py      # core logic
main.py        # CLI entry
debug.py       # diagnostics
Modelfile      # model config
```

---

## 🔮 Future Ideas (Experimental)

* Image input (Gemma multimodal)
* Video frame analysis
* Better file context handling
* Faster streaming modes

---

## 👤 Author

Vicky404
https://github.com/Vicky404-git

---

## 🧨 Note

Clanka is an experiment.

It’s built to explore:

* local LLMs
* terminal interfaces
* file-aware AI

If it breaks, that’s part of the process.

