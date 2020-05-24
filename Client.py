import argparse
import requests
import sys
import phrases
import pages

def create_main_parser(defaulthost, defaultport):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=defaulthost)
    parser.add_argument('--port', default=defaultport, type=int)
    return parser.parse_args()


def get_in(login, password, adress):
    answer = requests.get(f'{adress}/{pages.autification_page}', params = dict(login = login, password = password)).text
    return answer == 'True'


def exit_with_question():
    while True:
        answer = input(phrases.ask_again)
        if answer == 'Y':
            print(phrases.permission_given)
            exit()
        elif answer == 'N':
            print(phrases.permission_not_given)
            break
        else:
            print(phrases.command_doesnt_exist)


def create_login(login, password, adress):
    answer = requests.post(f'{adress}/{pages.autification_page}', params = dict(login = login, password = password)).text
    return answer == 'True'


def check_tokens(username, adress):
    return int(requests.get(f'{adress}/{username}/{pages.tokens_page}').text)


def add_take_tokens(username, amount, adress):
    answer = requests.post(f'{adress}/{username}/{pages.tokens_page}', params = dict(amount = amount)).text
    return answer == 'True'


def play(username, colour, bet, adress, black_red_win, green_win):
    if add_take_tokens(username, -bet, adress):
        tokens = check_tokens(username, adress)
        print(f'{phrases.tokens_amount}{tokens}')
        results = (requests.get(f'{adress}/{username}/{pages.game_page}')).text
        result = results.split(' ')
        print(f'{phrases.play}{result[1]} , {result[0]}!')
        if colour == result[0]:
            print(win)
            if colour == 'black' or colour == 'red':
                add_take_tokens(username, black_red_win * bet, adress)
            else:
                add_take_tokens(username, green_win * bet, adress)
            tokens = check_tokens(username, adress)
        else:
            print(phrases.lose)
        return True
    else:
        print(phrases.wrong_bet)
        return False


def login_help():
    print(phrases.help_new)
    print(phrases.help_login)
    print(phrases.help_exit)


def play_help():
    print(phrases.help_show)
    print(phrases.help_add)
    print(phrases.help_play)


defaulthost = 'localhost'
defaultport = 8000
black_red_win = 2
green_win = 14

parser = create_main_parser(defaulthost, defaultport)
adress = f'http://{parser.host}:{parser.port}'
login = ''

while True:
    command = input(phrases.ask_command)
    if command == 'help':
        login_help()
    elif command == 'new':
        login = input(phrases.ask_new_login)
        password = input(phrases.ask_password)
        if not create_login(login, password, adress):
            print(phrases.login_already_exist)
    elif command == 'exit':
        exit_with_question()
    elif command == 'login':
        login = input(phrases.ask_login)
        password = input(phrases.ask_password)
        answer = get_in(login, password, adress)
        if answer:
            print(f'{phrases.greatings}{login}!')
            break
        else:
            print(phrases.wrong_password_login)
    else:
        print(phrases.command_doesnt_exist)


while True:
    command = input(phrases.ask_command)
    if command == 'help':
        play_help()
    elif command == 'show':
        tokens = check_tokens(login, adress)
        print(f'{phrases.tokens_amount}{tokens}')
    elif command == 'add':
        amount = int(input(phrases.ask_amount))
        if amount <= 0:
            print(phrases.wrong_amount)
        else:
            add_take_tokens(login, amount, adress)
    elif command == 'exit':
        exit()
    elif command == 'play':
        bet = int(input(phrases.ask_bet))
        colour = str(input(phrases.ask_colour))
        play(login, colour, bet, adress, black_red_win, green_win)
    else:
        print(phrases.command_doesnt_exist)
