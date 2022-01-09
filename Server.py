# Wongsakorn Pinvasee 6210400175
# Tananat Kometjamikorn 6210406581

import socket
from _thread import *
import time
import _pickle as pickle

from ServerFUNCTION.BG import *


sc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

HOST = "127.0.0.1"
PORT = 8082

start = False

try:
    sc.bind((HOST, PORT))
except socket.error as e:
    print(e)
    print("[SERVER!!!!] => Server Can't Start")
    quit()

sc.listen()

print(f"[SERVER] => Server IP is " + str(HOST))

players = {}
connection = 0
player_id = 0


def setup_player(_id, deck):

    deck = re_deck(deck)
    host_cards = [pick_card(deck) for _ in range(2)]
    my_cards = [pick_card(deck) for _ in range(2)]

    host_score = calculate_score(host_cards)
    my_score = calculate_score(my_cards)

    end = 0
    rs = ""

    if check_blackjack(host_cards):
        end = 1
        rs = "Host got BlackJack You Lose!"
    elif check_blackjack(my_cards):
        end = 1
        rs = "You got BlackJack You Win!"

    players[_id] = {"my_cards": my_cards,
                    "my_score": my_score,
                    "host_cards": host_cards,
                    "host_score": host_score,
                    "end": end,
                    "result": rs}


def threaded_client(conn, _id):
    global connection, players, start

    # set up new player after connect
    data = conn.recv(1024)
    name = data.decode("utf-8")
    print(f"[LOG] => {name} connected to the server.")
    conn.send(str.encode(str(_id)))

    deck = {"A": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "J": 4, "Q": 4, "K": 4}

    setup_player(_id, deck)

    """
    command
    - start
    - rematch
    - pick
    - notpick
    """
    while True:
        try:
            data = conn.recv(1024)

            if not data:
                break
            data = data.decode('utf-8')
            print(f"[LOG] => Received '{data}' from player id {_id}")

            if data.split(" ")[0] == "start":
                send_data = pickle.dumps(players[_id])
            elif data.split(" ")[0] == "rematch":
                setup_player(_id, deck)
                send_data = pickle.dumps(players[_id])
            elif data.split(" ")[0] == "pick":
                players[_id]["my_cards"].append(pick_card(deck))
                players[_id]["my_score"] = calculate_score(players[_id]["my_cards"])

                if check_busted(players[_id]['my_cards']):
                    players[_id]["end"] = 1
                    players[_id]["result"] = "You Busted"
                send_data = pickle.dumps(players[_id])

            else:
                while check_host(players[_id]['host_cards']):
                    players[_id]["host_cards"].append(pick_card(deck))
                players[_id]["host_score"] = calculate_score(players[_id]["host_cards"])
                players[_id]["end"] = 1
                players[_id]["result"] = result(players[_id]["my_cards"], players[_id]["host_cards"])
                send_data = pickle.dumps(players[_id])

            conn.send(send_data)
        except Exception as e:
            print(e)
            break
        time.sleep(0.001)

    print(f"[DISCONNECT] => {name} is disconnected.")
    connection -= 1
    del players[_id]
    conn.close()


print("[BLACKJACK_GAME] => BLACKJACK is Ready")
print("[SERVER] => Waiting for connection ....")

while True:
    host, addr = sc.accept()
    print(f"[CONNECTION] = Connected to: {addr}")

    if addr[0] == HOST and not start:
        start = True
        print("[BLACKJACK_GAME] => BLACKJACK is Started")

    connection += 1
    start_new_thread(threaded_client, (host, player_id))
    player_id += 1
