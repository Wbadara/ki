import socket
import threading
import sys
from des import encrypt, decrypt

SHARED_KEY = "RAHASIA1"
HOST = '127.0.0.1'
PORT = 65432

def receive_messages(client):
    while True:
        try:
            cipher_hex = client.recv(1024).decode('utf-8')
            if not cipher_hex:
                break
                
            plaintext = decrypt(cipher_hex, SHARED_KEY)
            
            sys.stdout.write('\r\033[K')
            print(f"[Server]: {plaintext}")
            # print(f"[Cipher Masuk]: {cipher_hex}")
            sys.stdout.write("Anda: ")
            sys.stdout.flush()
            
        except Exception as e:
            sys.stdout.write('\r\033[K')
            print("\nKoneksi terputus.")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print(f"=== Terhubung ke Server {HOST}:{PORT} ===\n")

    threading.Thread(target=receive_messages, args=(client,), daemon=True).start()

    while True:
        msg = input("Anda: ")
        if msg.lower() == 'exit':
            break
            
        cipher = encrypt(msg, SHARED_KEY)
        # print(f"[Cipher Keluar]: {cipher}")
        client.sendall(cipher.encode('utf-8'))

if __name__ == "__main__":
    start_client()
