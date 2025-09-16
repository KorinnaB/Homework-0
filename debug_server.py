import socket
"""Testing the ports on my laptop feel free to ignore this file"""
PORT = 5000

try:
    print("[DEBUG] Creating socket...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print(f"[DEBUG] Binding to port {PORT}...")
    server_socket.bind(("0.0.0.0", PORT))
    
    print("[DEBUG] Listening for connections...")
    server_socket.listen(1)
    
    print("[DEBUG] Waiting for a client to connect...")
    conn, addr = server_socket.accept()
    print(f"[DEBUG] Connection established with {addr}")
    
    # Receive one message
    msg = conn.recv(1024).decode()
    print(f"[DEBUG] Received: {msg}")

except Exception as e:
    print(f"[ERROR] {e}")
finally:
    server_socket.close()
    print("[DEBUG] Server closed")
