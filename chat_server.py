import socket
import sys
import threading

def handle_client(conn):
    """ 
    CSCI4406 - Fall 25
    Korinna B., Charisma R., Allison H., Emma W. 
    - Receive messages from the client and print them
    - Once launched, the server waits for connection on the given port
    - python chat_server.py listen_port (to launch chat_server)
    - python chat_client.py server_ip server_port (to launch chat_client)
    - Make sure it runs on Linux
    """
    try:
        while True:
            data = conn.rev(1024) 
            if not data:
                break
            print(data.decode(), end="")
    except:
        pass
    finally:
        conn.close()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} listen_port")
        sys.exit(1)
        
        listen_port = int(sys.argv[1])

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("0.0.0.0", listen_port))
        server_socket.listen(1)
        