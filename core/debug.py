import sys
import os
import time
import shutil
import platform

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
CYAN = '\033[96m'
RESET = '\033[0m'

def ok(msg): print(f"{GREEN}[OK]{RESET} {msg}")
def fail(msg): print(f"{RED}[FAIL]{RESET} {msg}")
def warn(msg): print(f"{YELLOW}[WARN]{RESET} {msg}")

print(f"{CYAN}=================================================={RESET}")
print(f"{CYAN}      CLANKA PRE-FLIGHT DIAGNOSTICS v2.0          {RESET}")
print(f"{CYAN}=================================================={RESET}\n")

time.sleep(0.3)

# =========================
# 1. PYTHON CHECK
# =========================
print(f"{YELLOW}[*] Python Engine{RESET}")
if sys.version_info >= (3, 10):
    ok(f"Python {sys.version.split()[0]}")
else:
    fail("Python 3.10+ required")
    sys.exit(1)

# =========================
# 2. DEPENDENCIES
# =========================
print(f"\n{YELLOW}[*] Dependencies{RESET}")
deps = ['rich', 'ollama', 'psutil']
missing = []

for dep in deps:
    try:
        __import__(dep)
        ok(dep)
    except ImportError:
        fail(dep)
        missing.append(dep)

if missing:
    print(f"\n{RED}Install missing deps:{RESET}")
    print(f"pip install {' '.join(missing)}")
    sys.exit(1)

# =========================
# 3. OLLAMA CHECK
# =========================
print(f"\n{YELLOW}[*] Ollama Daemon{RESET}")
import ollama

try:
    models = ollama.list()
    ok("Daemon responding")

    if 'clanka' in str(models).lower():
        ok("Model 'clanka' found")
    else:
        fail("Model 'clanka' missing")
        print("Run: ollama create clanka -f Modelfile")
        sys.exit(1)

except Exception as e:
    fail("Ollama not running")
    print(f"Error: {e}")
    sys.exit(1)

# =========================
# 4. INFERENCE TEST
# =========================
print(f"\n{YELLOW}[*] Inference Test{RESET}")


print(f"\n Cheking Clanka")
try:
    start = time.time()
    res = ollama.generate(
        model="clanka",
        prompt="Reply ONLY with OK"
    )
    latency = round(time.time() - start, 2)

    if "ok" in res['response'].lower():
        ok(f"Inference working ({latency}s)")
    else:
        warn("Model responded unexpectedly")

except Exception as e:
    fail(f"Inference failed: {e}")
    sys.exit(1)


# =========================
# 5. FILE SYSTEM CHECK
# =========================
print(f"\n{YELLOW}[*] File System{RESET}")

test_file = "clanka_test.tmp"
try:
    with open(test_file, "w") as f:
        f.write("test")

    os.remove(test_file)
    ok("Read/Write permissions OK")

except Exception:
    fail("Cannot write files in this directory")
    sys.exit(1)

# =========================
# 6. CLI CHECK
# =========================
print(f"\n{YELLOW}[*] CLI Command{RESET}")

if shutil.which("clanka"):
    ok("clanka command available")
else:
    warn("clanka alias not set (optional)")

# =========================
# 7. PATCH SAFETY TEST
# =========================
print(f"\n{YELLOW}[*] Patch Safety Test{RESET}")

sample_code = "x = 10\ny = 0\nprint(x/y)"

try:
    compile(sample_code, "<test>", "exec")
    ok("Compile system OK")
except:
    fail("Python compile failed")

# =========================
# DONE
# =========================
print(f"\n{GREEN}=================================================={RESET}")
print(f"{GREEN} [READY] Clanka is fully operational.{RESET}")
print(f"{GREEN}=================================================={RESET}")
