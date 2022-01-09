# Wongsakorn Pinvasee 6210400175
# Tananat Kometjamikorn 6210406581

import pyfiglet
from colorama import Fore
from colorama import Style

from Client import Network


def blackjack(name, host, port):
    server = Network(host, port)
    server.connect(name)

    print(f"{Fore.RED}{'=' * 108}{Style.RESET_ALL}")
    title = pyfiglet.figlet_format("BLACK\nJACK", font="5lineoblique")
    print(f"{Fore.GREEN} {title} {Style.RESET_ALL}")
    print(f"{Fore.RED}{'=' * 108}{Style.RESET_ALL}")

    print(f"Hello {name}!!!")
    print("Welcome to play the BLACKJACK game.")
    ready = input("Are you ready? (Y/N): ").lower()

    print(" ")

    if ready.lower() == "n":
        server.disconnect()
        return 0

    info = server.send("start")

    while True:

        first_host_card = info['host_cards'][0]
        print(f"{Fore.BLUE}First host card: [{first_host_card}]\n{Style.RESET_ALL}")

        while not info['end']:
            my_cards = info['my_cards']
            my_score = info['my_score']

            print(f"{Fore.YELLOW}Your hand is: {my_cards}, Score: {my_score}{Style.RESET_ALL}")

            pick = input("Do you want to pick more card? (Y/N): ").lower()

            if pick.lower() == "n":
                info = server.send("notpick")
            else:
                info = server.send("pick")

        my_cards = info["my_cards"]
        my_score = info["my_score"]
        host_cards = info['host_cards']
        host_score = info['host_score']
        result = info['result']

        print(f"\n{Fore.BLUE}[Result]")
        print(f"Your final hand: {my_cards}, Score: {my_score}")
        print(f"Host final hand: {host_cards}, Score: {host_score}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}{result}{Style.RESET_ALL}")
        print("-" * 108)
        ready = input("Do you want to play more? (Y/N): ").lower()
        if ready.lower() == "n":
            break
        info = server.send("rematch")
        print(" ")

    server.disconnect()
    print(f"{Fore.GREEN}Good Bye {name}. See you next time.{Style.RESET_ALL}")


if __name__ == "__main__":
    host = input("Host: ")
    port = int(input("Port: "))
    username = input("Your username: ")

    blackjack(username, host, port)
