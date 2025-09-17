import socket
import threading
import sys
import os
import shutil


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
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

def display_line(prefix, buffer):

    width = shutil.get_terminal_size().columns
    if len(buffer) > width - len(prefix) - 1:
        buffer = buffer[-(width - len(prefix) - 1):]
    print(f"\r{prefix}{buffer}{' ' * 5}", end="", flush=True)

def receive_messages(sock):
    buffer = ""
    prefix = "[SERVER] "
    try:
        while True:
            data = sock.recv(1024)
            if not data:
                print("\n[CLIENT] Server disconnected")
                break
            for c in data.decode():
                if c in ("\r", "\n"):
                    print(f"\r{' ' * 50}") # clears line
                    print(f"\n{prefix}{buffer}")
                    buffer = ""
                elif c == "\x08":
                    buffer = buffer[:-1]
                else:
                    buffer += c
                display_line(prefix, buffer)
    except Exception as e:
        print(f"\n[CLIENT ERROR] {e}")
    finally:
        sock.close()

def main():
    if len(sys.argv) != 3:
        print(f"Usage: python {sys.argv[0]} server_ip server_port")
        sys.exit(1)

    SERVER_IP = sys.argv[1]
    SERVER_PORT = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((SERVER_IP, SERVER_PORT))
    print(f"[CLIENT] Connected to {SERVER_IP}:{SERVER_PORT}")
    print("[CLIENT] Type your messages below:")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start()

    buffer = ""
    prefix = "[CLIENT] "

    try:
        while True:
            char = get_char()
            if char in ("\r", "\n"):
                sock.sendall(b"\n")
                buffer = "" 
                print() # new line for spacing
            elif char == "\x08":
                buffer = buffer[:-1]
                sock.sendall(char.encode())
            else:
                buffer += char
                sock.sendall(char.encode())
            display_line(prefix, buffer)
    except KeyboardInterrupt:
        print("\n[CLIENT] Shutting down...")
    finally:
        sock.close()

if __name__ == "__main__":
    main()
