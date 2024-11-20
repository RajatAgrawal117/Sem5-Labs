import socket

def udp_server():
    # Define server's IP address and port
    server_ip = '127.0.0.1'  # Localhost
    server_port = 12345  # Port to bind

    # Create a UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the IP and port
    sock.bind((server_ip, server_port))

    print(f"UDP Server is up and listening on {server_ip}:{server_port}...")

    while True:
        # Receive data from the client
        data, client_address = sock.recvfrom(1024)  # Buffer size of 1024 bytes
        message = data.decode('utf-8')
        print(f"Received message from {client_address}: {message}")

        # Send an acknowledgment back to the client
        ack_message = f"ACK: Message '{message}' received"
        sock.sendto(ack_message.encode('utf-8'), client_address)

if __name__ == "__main__":
    udp_server()