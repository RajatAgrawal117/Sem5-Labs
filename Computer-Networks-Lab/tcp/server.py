import socket
import threading
import time

def handle_client(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                print("Client disconnected.")
                break
            message = data.decode('utf-8')
            if message.lower() == "exit":
                print("Client requested disconnection.")
                break
            print(f"Received message from client: {message}\n")
        except ConnectionResetError:
            print("Connection lost.")
            break
    client_socket.close()

def send_message_to_client(client_socket):
    while True:
        try:
            response = input("Enter message to send to client: \n")
            if response.lower() == "exit":
                print("Disconnecting from client.")
                client_socket.sendall(response.encode('utf-8'))
                break
            client_socket.sendall(response.encode('utf-8'))
        except ConnectionResetError:
            print("Failed to send. Client disconnected.")
            break
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        print("Setting up connection, please wait...")
        time.sleep(2)
        print("Connection setup complete.")
        
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()
        message_sender = threading.Thread(target=send_message_to_client, args=(client_socket,))
        message_sender.start()

if __name__ == "__main__":
    main()