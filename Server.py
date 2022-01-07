import socket

from blackjack import *

deck = {"A": 4, "2": 4, "3": 4, "4": 4, "5": 4, "6": 4, "7": 4, "8": 4, "9": 4, "10": 4, "J": 4, "Q": 4, "K": 4}
card_score = {"A": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "J": 10, "Q": 10,
              "K": 10}


def start_to_play(client):
    end_game = False

    host_card = [pick_card() for _ in range(2)]
    user_card = [pick_card() for _ in range(2)]

    while not end_game:
        msg = ("The first host's card: [" + host_card[0] + "]\n").encode("utf-8")
        client.send(msg)
        client.send(
            ("Your hand is :" + str(user_card) + ", and score is: " + str(calculate_score(user_card)) + "\n").encode("utf-8"))

        if check_blackjack(host_card):
            open_card(user_card, host_card)
            client.send((open_card(user_card, host_card) + '\n' + "Host got BlackJack You Lose!").encode("utf-8"))
            end_game = True
            break

        elif check_blackjack(user_card):
            open_card(user_card, host_card)
            client.send((open_card(user_card, host_card) + '\n' + "User got BlackJack You Win!").encode("utf-8"))
            end_game = True
            break

        msg = client.send(("Do you want to pick more card (Y/N):").encode("utf-8"))

        need = client.recv(1024).decode('utf-8')
        print("User need more card: " + need)
        if not need: 
            print("Server is closing")
            break

        while True:
            if need.lower() == "y":
                user_card.append(pick_card())
                if check_busted(calculate_score(user_card)):
                    client.send(("0" + open_card(user_card, host_card) + '\n' +"You busted").encode("utf-8"))
                    end_game = True
                    break
                break
            elif need.lower() == "n":
                while check_host(host_card):
                    host_card.append(pick_card())

                client.send(
                    ("0" + open_card(user_card, host_card) + '\n' + result(user_card, host_card) + '\n').encode("utf-8"))
                end_game = True
                break
            else:
                client.send("Please type again only (Y/N): ".encode("utf-8"))
    re_deck()


def main_run():
    host = "127.0.0.1"  # ip
    port = 8082
    server = socket.socket()
    server.bind((host, port))
    server.listen(1)  # assign number of client
    print("wait for connect from client")
    client, addr = server.accept()
    print("Connect From: " + str(addr))

    # transfer data
    while True:
        # receive data from client
        data = client.recv(1024).decode('utf-8')  # Welcome blackjack do you want to play client
        
        if not data:
            break
        
        print("User want to play: " + data)
        if data.lower() == "y":
            playmore = 'y'
            while playmore == 'y':
                start_to_play(client)
                print("---------------------------------------------------------------")
                playmore = client.recv(1024).decode("utf-8").lower()
                if not playmore:
                    break
                print("User type playmore: " + playmore)
                if playmore == 'n':
                    server.close()
                    break

        # if data.lower() == "n":
        #     print("Server is close")
        #     server.close()


if __name__ == "__main__":
    main_run()
