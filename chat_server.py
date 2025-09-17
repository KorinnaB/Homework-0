"""
CSCI 4406 - Fall 2025
Team members: Korinna B., Charisma R., Allison H., Emma W.

"""
import socket
import threading
import sys
import os
import shutil

# Cross-platform single-character input
if os.name == "nt": # windows
    import msvcrt

    def get_char():
        return msvcrt.getwch()
else:
    import termios # unix api for terminal i/o
    import tty

    def get_char(): # get a single character from stdin
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

def display_line(prefix, buffer): # displays the current line with prefix and handles line width
   
    width = shutil.get_terminal_size().columns # get terminal width

    if len(buffer) > width - len(prefix) - 1: # account for prefix and a space
        buffer = buffer[-(width - len(prefix) - 1):] 
    print(f"\r{prefix}{buffer}{' ' * 5}", end="", flush=True) # extra spaces to clear remnants of previous longer lines

def receive_messages(conn): # thread function to receive messages from client
    buffer = ""
    prefix = "[CLIENT] "
    try: # main receive loop
        while True:
            data = conn.recv(1024) # receive data from client
            if not data: # connection closed
                print("\n[SERVER] Client disconnected")
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
        print(f"\n[SERVER ERROR] {e}")
    finally:
        conn.close()

def main(): # main server function
    if len(sys.argv) != 2: # check for correct args
        print(f"Usage: python {sys.argv[0]} listen_port")
        sys.exit(1) # if not correct args, exit

    PORT = int(sys.argv[1]) # get port from args

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create TCP socket
    server_socket.bind(("0.0.0.0", PORT)) # bind to all interfaces on specified port
    server_socket.listen(1) # listen for incoming connections
    print(f"[SERVER] Listening on port {PORT}...") 
 
    conn, addr = server_socket.accept() # accept a connection
    print(f"[SERVER] Connection established with {addr}") 

    threading.Thread(target=receive_messages, args=(conn,), daemon=True).start() # start receive thread

    print("[SERVER] Type your messages below:")
    buffer = ""
    prefix = "[SERVER] "

    try: # main input loop
        while True:
            char = get_char() # get single character input
            if char in ("\r", "\n"): # newline or return
                conn.sendall(b"\n") # send newline to client
                buffer = "" # reset buffer
                print() # new line for spacing
            elif (char == "\x08" or char == "\x7f"): # detects ascii backspace or delete on macos
                buffer = buffer[:-1] # remove last char from buffer
                conn.sendall(char.encode()) # send backspace to client
            else:
                buffer += char # add char to buffer
                conn.sendall(char.encode()) # send char to client
            display_line(prefix, buffer) # update display

    except KeyboardInterrupt:
        print("\n[SERVER] Shutting down...")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    main()
