# Wongsakorn Pinvasee 6210400175
# Tananat Kometjamikorn 6210406581

import socket
import _pickle as pickle


class Network:

    def __init__(self, host, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (self.host, self.port)

    def connect(self, name):
        self.client.connect(self.addr)
        self.client.send(str.encode(name))
        data = self.client.recv(1024)
        # print("[LOG] => Received '" + data.decode() + "' from server")
        return int(data.decode())

    def disconnect(self):
        self.client.close()

    def send(self, data, is_pickle=False):
        try:
            if is_pickle:
                self.client.send(pickle.dumps(data))
            else:
                self.client.send(str.encode(data))
            reply = self.client.recv(1024*4)
            try:
                reply = pickle.loads(reply)
            except Exception as e:
                print(e)

            # print("[LOG] Received ", reply, " from server")
            return reply
        except socket.error as e:
            print(e)

