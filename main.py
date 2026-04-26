import sys
import subprocess
from core.clanka import stream_response, handle_wtf, handle_patch
import os

BASE = os.path.dirname(__file__)

def run():
    args = sys.argv[1:]

    if not args:
        print("Usage: clanka 'msg' | clanka wtf [file] | clanka patch file.py")
        return

    cmd = args[0].lower()

    if cmd == "wtf":
        handle_wtf(args[1] if len(args) > 1 else None)

    elif cmd == "patch":
        if len(args) > 1:
            handle_patch(args[1])
        else:
            print("Usage: clanka patch file.py")

    elif cmd == "debug":
        subprocess.run(["python3", os.path.join(BASE, "core/debug.py")])

    else:
        stream_response(" ".join(args))

if __name__ == "__main__":
    run()
