import socket
import threading
import sys
import os
import shutil

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
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

def display_line(prefix, buffer):
   
    width = shutil.get_terminal_size().columns

    if len(buffer) > width - len(prefix) - 1:
        buffer = buffer[-(width - len(prefix) - 1):]
    print(f"\r{prefix}{buffer}{' ' * 5}", end="", flush=True)

def receive_messages(conn):
    buffer = ""
    prefix = "[CLIENT] "
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                print("\n[SERVER] Client disconnected")
                break
            for c in data.decode():
                if c in ("\r", "\n"):
                    print(f"\r{' ' * 50}") # clears line
                    print(f"\n{prefix}{buffer}")
                    buffer = ""
                elif c == "\x08":  # Backspace
                    buffer = buffer[:-1]
                else:
                    buffer += c
                display_line(prefix, buffer)
    except Exception as e:
        print(f"\n[SERVER ERROR] {e}")
    finally:
        conn.close()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} listen_port")
        sys.exit(1)

    PORT = int(sys.argv[1])


    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(1)
    print(f"[SERVER] Listening on port {PORT}...")

    conn, addr = server_socket.accept()
    print(f"[SERVER] Connection established with {addr}")

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start()

    print("[SERVER] Type your messages below:")
    buffer = ""
    prefix = "[SERVER] "
    try:
        while True:
            char = get_char()
            if char in ("\r", "\n"):
                conn.sendall(b"\n")
                buffer = ""
                print() # new line for spacing
            elif char == "\x08":
                buffer = buffer[:-1]
                conn.sendall(char.encode())
            else:
                buffer += char
                conn.sendall(char.encode())
            display_line(prefix, buffer)
    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    main()
