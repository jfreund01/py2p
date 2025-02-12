import socket
import threading
import time
import sys
import uuid
import argparse
import readline

# Define and generate random uuid64 for client identification

uuid64 = uuid.uuid4()

def recieve_message(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if not message:
                break
            
            # save input

            saved_input = readline.get_line_buffer()
            # clear current line and print message
            print("\r\033[K", end="")
            print(f"\r[PEER]: {message}")

        except:
            break
    sock.close()

def send_message(sock):
    while True:
        message = input()
        sock.sendall(message.encode())
        if message == "exit":
            break
    sock.close()

def peer_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", port))
    server_socket.listen(5)
    print(f"Server listening on port {port}")
    while True:
        client_socket, address = server_socket.accept()
        print(f"Connection established with {address}") 
        threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

def peer_client(peer_ip, peer_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((peer_ip, peer_port))
    print(f"Connected to {peer_ip}:{peer_port}")

    threading.Thread(target=recieve_message, args=(sock,), daemon=True).start()
    send_message(sock)

    

def handle_client(client_socket):

    print(f"Connected established with {client_socket}")
    threading.Thread(target=recieve_message, args=(client_socket,), daemon=True).start()

    send_message(client_socket)

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="Server port", type=int, required=True)
    parser.add_argument("-c", "--client", help="Client port", type=int, required=False)
    args = parser.parse_args()
    server_port = args.server
    threading.Thread(target=peer_server, args=(server_port,)).start()
        
    if args.client:
        client_port = args.client
        peer_client("localhost", client_port)



    
