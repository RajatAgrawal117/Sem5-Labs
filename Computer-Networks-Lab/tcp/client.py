import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')
            if message.lower() == "exit":
                break
        except:
            break
    client_socket.close()

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 12345
    client_socket.connect((host, port))
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    while True:
        message = input("Enter your message (or exit): \n")
        if message.lower() == "exit":
            client_socket.sendall(message.encode('utf-8'))
            break
        client_socket.sendall(message.encode('utf-8'))

if __name__ == "__main__":
    main()
