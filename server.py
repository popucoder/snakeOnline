import socket
from _thread import *
import pickle


server = "127.0.0.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")


player = [(1,2), (2,3)]
def threaded_client(conn, p):
    
    conn.send(pickle.dumps(player[p]))
    
    while True:
        try:
            data = pickle.loads(conn.recv(4096))

            if not data:
                break

            else:
                print("Data from client ", data)
                conn.sendall(pickle.dumps(player[p]))

        except:
            break

    print("Lost connection")
    conn.close()


client_number = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, client_number))
    client_number+=1

