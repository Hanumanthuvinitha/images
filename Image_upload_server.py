# tcp_image_server.py
import socket
import os
from datetime import datetime

HOST = ''           # Listen on all interfaces
PORT = 60001
IMAGE_DIR = 'images'

def start_server():
    os.makedirs(IMAGE_DIR, exist_ok=True)  # Create directory if it doesn't exist

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(2)
        print(f"Listening on port {PORT}...")

        while True:
            conn, addr = s.accept()
            print(f"Connected by {addr}")

            img_size_bytes = conn.recv(4)
            if not img_size_bytes:
                conn.close()
                continue

            img_size = int.from_bytes(img_size_bytes, 'big')
            print(f"Expecting image of size: {img_size} bytes")

            img_data = b''
            while len(img_data) < img_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                img_data += packet

            if img_data:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = os.path.join(IMAGE_DIR, f'image_{timestamp}.jpg')
                with open(filename, 'wb') as f:
                    f.write(img_data)
                print(f"Saved {filename}")

            conn.close()

if __name__ == "__main__":
    start_server()
