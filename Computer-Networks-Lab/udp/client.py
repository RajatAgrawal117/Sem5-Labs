import socket

def udp_client():
    server_ip = '127.0.0.1'
    server_port = 12345
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        while True:
            message = input("Enter message to send to the server (or 'exit' to quit): ")

            if message.lower() == 'exit':
                print("Exiting...")
                break

                # Send message to server
            sock.sendto(message.encode('utf-8'), (server_ip, server_port))

            try:
                    # Receive acknowledgment
                data, server = sock.recvfrom(1024)
                print(f"Received acknowledgment from server: {data.decode('utf-8')}")
            except Exception as e:
                print(f"Error receiving acknowledgment: {e}")
    except Exception as e:
        print(f"Error in client communication: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
        udp_client()