import socket
import threading
import sys
import os

# Cross-platform single-character input
if os.name == "nt":
    import msvcrt
    def get_char():
        return msvcrt.getwch()
else:
    import termios
    import tty
    def get_char():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

LOCAL_PREFIX = "[CLIENT] "
REMOTE_PREFIX = "[SERVER] "

local_buffer = ""  # global buffer for the typing line

def print_buffer():
    """Print local buffer after remote message arrives."""
    global local_buffer
    print(f"\r{LOCAL_PREFIX}{local_buffer}", end="", flush=True)

def receive_messages(sock):
    """Receive messages from server and print them above local buffer."""
    buffer = ""
    global local_buffer
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print(f"\n{LOCAL_PREFIX} Server disconnected")
                break
            for c in data.decode():
                if c in ("\r", "\n"):
                    if buffer:
                        print(f"\n{REMOTE_PREFIX}{buffer}")
                        buffer = ""
                        print_buffer()
                elif c == "\x08":
                    buffer = buffer[:-1]
                else:
                    buffer += c
        except:
            break

def main():
    global local_buffer
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} server_ip server_port")
        sys.exit(1)

    SERVER_IP = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    print(f"{LOCAL_PREFIX} Connected to {SERVER_IP}:{SERVER_PORT}")
    print(f"{LOCAL_PREFIX} Type your messages below:")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    try:
        while True:
            char = get_char()
            if char in ("\r", "\n"):
                print(f"\n{LOCAL_PREFIX}{local_buffer}")
                local_buffer = ""
            elif char == "\x08":
                local_buffer = local_buffer[:-1]
                sock.sendall(char.encode())
            else:
                local_buffer += char
                sock.sendall(char.encode())
            print_buffer()
    except KeyboardInterrupt:
        print(f"\n{LOCAL_PREFIX} Shutting down...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
