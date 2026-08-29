import sys
import subprocess
import os

from core.clanka import stream_response, handle_wtf, handle_patch
from core import config as cfg
from core import rag

BASE = os.path.dirname(__file__)


def _print(msg):
    print(msg)


def run():
    args = sys.argv[1:]

    if not args:
        print(
            "Usage:\n"
            "  clanka 'msg'              chat\n"
            "  clanka wtf [file]         explain a file or the project\n"
            "  clanka patch file.py      refactor a file\n"
            "  clanka index [dir]        (re)build the code/doc index\n"
            "  clanka config --mem N     set resource budget (5-100)\n"
            "  clanka config             show current config\n"
            "  clanka debug              run pre-flight diagnostics"
        )
        return

    cmd = args[0].lower()

    if cmd == "wtf":
        handle_wtf(args[1] if len(args) > 1 else None)

    elif cmd == "patch":
        if len(args) > 1:
            handle_patch(args[1])
        else:
            print("Usage: clanka patch file.py")

    elif cmd == "index":
        directory = args[1] if len(args) > 1 else "."
        rag.build_index(directory, on_progress=_print)

    elif cmd == "config":
        if len(args) > 2 and args[1] == "--mem":
            try:
                config = cfg.set_mem_percent(args[2])
                print(f"mem_percent set to {config['mem_percent']}")
            except ValueError as e:
                print(f"Error: {e}")
        else:
            config = cfg.load_config()
            for k, v in config.items():
                print(f"{k}: {v}")

    elif cmd == "debug":
        subprocess.run(["python3", os.path.join(BASE, "core", "debug.py")])

    else:
        stream_response(" ".join(args))


if __name__ == "__main__":
    run()
