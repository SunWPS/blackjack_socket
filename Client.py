# วงศกร ปิ่นวาสี 6210400175
# ธนณัฏฐ์ โกเมศจามิกรณ์ 6210406581


import socket
import re


def main_run():
    host = input("Type host: ")
    port = int(input("Type port: "))
    server = socket.socket()
    server.connect((host, port))

    print("Welcome To blackjack.")

    play = input("Do you want to play? (y/n): ").lower()
    if play == 'y':
        server.send(play.encode('utf-8'))
        while play == "y":
            data = server.recv(1024).decode('utf-8')

            if re.match(r"^0", data):  # result print
                print(data[1:])
            else:
                print(data)

            if "(Y/N)" in data:
                data = input()
                server.send(data.encode('utf-8'))
            if re.match(r"^0", data) or "BlackJack" in data:
                print("------------------------------------------------")
                play = input("Do you want to play more? (y/n): ").lower()
                if play == 'n':
                    print("Goodbye")
                    server.close()
                else:
                    server.send(play.encode("utf-8"))
                    data = server.recv(1024).decode('utf-8')
                    print(data)
    else:
        server.send(play.encode('utf-8'))
        print("Goodbye")
        server.close()


if __name__ == "__main__":
    main_run()
