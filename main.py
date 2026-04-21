import sys
import os
from clanka import stream_response, handle_wtf, handle_patch
def run():
    args = sys.argv[1:]
    
    if not args:
        print("Usage: clanka 'message' OR clanka wtf [file]")
        return

    
    command = args[0].lower()
    
    if command == "wtf":
        if len(args) > 1:
            handle_wtf(args[1])
        else:
            handle_wtf()

    elif command == "patch":
        if len(args) > 1:
            handle_patch(args[1])
        else:
            print("Usage: clanka patch file.py")
    elif command == "debug":
        os.system("python3 debug.py")
    else:
        stream_response(" ".join(args))

if __name__ == "__main__":
    run()
