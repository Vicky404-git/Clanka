import sys
from clanka import stream_response

def run():
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
        stream_response(user_input)
    else:
        print("Usage: clanka 'message'")

if __name__ == "__main__":
    run()
