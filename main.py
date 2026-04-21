import sys
from clanka import stream_response, handle_wtf

def run():
    args = sys.argv[1:]
    
    if not args:
        print("Usage: clanka 'message' OR clanka wtf [file]")
        return

    # Check for the 'wtf' codebase analyzer mode
    if args[0].lower() == "wtf":
        if len(args) > 1:
            handle_wtf(args[1]) # clanka wtf script.py
        else:
            handle_wtf()        # clanka wtf (current dir)
    else:
        # Standard chat mode
        user_input = " ".join(args)
        stream_response(user_input)

if __name__ == "__main__":
    run()
