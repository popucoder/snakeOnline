import socket
import pickle

server = "127.0.0.1"
port = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


client.connect((server, port))
data = pickle.loads(client.recv(4096))
print(data)

while True:
    client.sendall(pickle.dumps((1,3)))
    client.recv(4096)
    input()