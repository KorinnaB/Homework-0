import socket
import threading
import sys
import os
import shutil

# Cross-platform single-character input
if os.name == "nt": # windows
    import msvcrt # windows api for terminal i/o

    def get_char(): # get a single character from stdin
        return msvcrt.getwch() # getwch() to support unicode
else:
    import termios # unix api for terminal i/o
    import tty # unix api for terminal i/o

    def get_char():
        fd = sys.stdin.fileno() # get file descriptor for stdin
        old_settings = termios.tcgetattr(fd) # save old terminal settings
        try: # set terminal to raw mode to capture single char
            tty.setraw(fd)
            char = sys.stdin.read(1) 
        finally: # restore old terminal settings
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

def display_line(prefix, buffer): # displays the current line with prefix and handles line width

    width = shutil.get_terminal_size().columns # get terminal width
    if len(buffer) > width - len(prefix) - 1: 
        buffer = buffer[-(width - len(prefix) - 1):] 
    print(f"\r{prefix}{buffer}{' ' * 5}", end="", flush=True) # extra spaces to clear remnants of previous longer lines

def receive_messages(sock): # thread function to receive messages from server
    buffer = "" # current line buffer
    prefix = "[SERVER] " # prefix for server messages
    try: # main receive loop
        while True:
            data = sock.recv(1024) # receive data from server
            if not data: # connection closed
                print("\n[CLIENT] Server disconnected")
                break
            for c in data.decode(): # process each character
                if c in ("\r", "\n"): # newline or return
                    print(f"\r{' ' * 50}") # clears line
                    print(f"\n{prefix}{buffer}") # print the complete line
                    buffer = "" # reset buffer
                elif (c == "\x08" or c == "\x7f"):  # detects ascii backspace or delete on macos
                    buffer = buffer[:-1] # remove last char entered
                else:
                    buffer += c # add char to buffer
                display_line(prefix, buffer) # update display

    except Exception as e: # catch any errors
        print(f"\n[CLIENT ERROR] {e}")
    finally: 
        sock.close() # ensure socket is closed

def main(): # main client function
    if len(sys.argv) != 3: # check for correct args
        print(f"Usage: python {sys.argv[0]} server_ip server_port")
        sys.exit(1) # if not correct args, exit

    SERVER_IP = sys.argv[1] 
    SERVER_PORT = int(sys.argv[2])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create TCP socket
    sock.connect((SERVER_IP, SERVER_PORT)) # connect to server
    print(f"[CLIENT] Connected to {SERVER_IP}:{SERVER_PORT}") # connection success message
    print("[CLIENT] Type your messages below:")

    threading.Thread(target=receive_messages, args=(sock,), daemon=True).start() # start receive thread

    buffer = ""
    prefix = "[CLIENT] " # prefix for client messages

    try: # main input loop
        while True:
            char = get_char() # get single character input
            if char in ("\r", "\n"): # newline or return
                sock.sendall(b"\n") # send newline to server
                buffer = "" # reset buffer
                print() # new line for spacing
            elif (char == "\x08" or char == "\x7f"):  # detects ascii backspace or delete on macos
                buffer = buffer[:-1] # remove last char from buffer
                sock.sendall(char.encode()) # send backspace to server
            else:
                buffer += char # add char to buffer
                sock.sendall(char.encode()) # send char to server
            display_line(prefix, buffer) # update display

    except KeyboardInterrupt:
        print("\n[CLIENT] Shutting down...")
    finally:
        sock.close() # ensure socket is closed

if __name__ == "__main__":
    main()
