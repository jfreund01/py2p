import socket
import threading
import time
import os
import uuid
import argparse
import readline

# Define and generate random uuid64 for client identification

uuid64 = uuid.uuid4()

# recieved massages should always be:
# [PEER]: filename
# [PEER]: file_size
# [PEER]: file_data

def recieve_message(sock):
    while True:
        try:
            filename = sock.recv(1024).decode()
            file_size = int(sock.recv(1024).decode())
            print(f"Recieving file {filename} of size {file_size}")
            with open("recieved_data/" + filename, "wb") as file:
                while file_size > 0:
                    file_data = sock.recv(1024)
                    file_size -= len(file_data)
                    file.write(file_data)
        except:
            break
    # while True:
    #     try:
    #         message = sock.recv(1024).decode()
    #         if not message:
    #             break
            
    #         # save input

    #         saved_input = readline.get_line_buffer()
    #         # clear current line and print message
    #         print("\r\033[K", end="")
    #         print(f"\r[PEER]: {message}")

    #     except:
    #         break
    # sock.close()

def send_message(sock):
    while True:
        filename = input("> enter file name: ")
        file_path = "test_data/" + filename
        file_size = os.path.getsize(file_path)

        sock.send(filename.encode())
        sock.send(str(file_size).encode())
        time.sleep(0.1)
        with open(file_path, "rb") as file:
            file_data = file.read(1024)
            while file_data:
                sock.send(file_data)
                file_data = file.read(1024)
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



    
