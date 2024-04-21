import socket
import pickle
from helper_1 import TFML
import numpy as np

ClientSocket = socket.socket()
host = '127.0.0.1'
port = 1233
clientModel=TFML('client1')
print('Waiting for connection')

try:
    ClientSocket.connect((host, port))
except socket.error as e:
    print(str(e))

print("connection established")

old_client_weight=clientModel.model.get_weights()
new_client_weight=clientModel.model.get_weights()

while True:
    old_client_weight=new_client_weight
    old_client_weight.append(clientModel.name)
    ClientSocket.send(pickle.dumps(old_client_weight)+b'endingpickle')
    received_weights = b''
    while received_weights[-12:] != b'endingpickle':
        data = ClientSocket.recv(1024)
        received_weights += data
    received_weights = pickle.loads(received_weights[:-12])

    clientModel.model.set_weights(received_weights)
    clientModel.run()
    clientModel.eval()
    new_client_weight=clientModel.model.get_weights()

ClientSocket.close()