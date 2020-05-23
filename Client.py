import argparse
import requests
import sys


def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default = 'localhost')
    parser.add_argument('--port', default = 8000, type = int)
    return parser.parse_args()


def get_in(login, password, parser):
    answer = requests.get(f'http://{parser.host}:{parser.port}/autification', params = dict(login = login, password = password)).text
    return answer == 'True'


def exit_with_question():
    while True:
        answer = input('Are you sure about that?(Y/N)')
        if answer == 'Y':
            print('Ok, let\'s go!')
            exit()
        elif answer == 'N':
            print('Smart move')
            break
        else:
            print('Invalid command, I will ask again')

def create_login(login, password, parser):
    answer = requests.post(f'http://{parser.host}:{parser.port}/autification', params = dict(login = login, password = password)).text
    return answer == 'True'


def check_tokens(username, parser):
    return int(requests.get(f'http://{parser.host}:{parser.port}/{username}/tokens').text)


def add_take_tokens(username, amount, parser):
    answer = (requests.post(f'http://{parser.host}:{parser.port}/{username}/tokens', params = dict(amount = amount)).text)
    return answer == 'True'


def play(username, colour, bet, parser):
    if add_take_tokens(username, -bet, parser):
        tokens = check_tokens(username, parser)
        print(f'Your tokens for now: {tokens}')
        results = (requests.get(f'http://{parser.host}:{parser.port}/{username}/game')).text
        result = results.split(' ')
        print(f'The game goes on! Today it is {result[1]} , {result[0]}!')
        if colour == result[0]:
            print('You won!')
            if colour == 'black' or colour == 'red':
                add_take_tokens(username, 2 * bet, parser)
            else:
                add_take_tokens(username, 14 * bet, parser)
            tokens = check_tokens(username, parser)
        else:
            print('You lost(')
        return True
    else:
        print('Your bet is not correct(')
        return False


def login_help():
    print('new - create login and password')
    print('login - login into system')
    print('exit - quit')


def play_help():
    print('show - show the amount of tokens')
    print('add - add some tokens')
    print('play - go to table and play')


parser = create_main_parser()
login = ''
while True:
    command = input('Write the comand> ')
    if command == 'help':
        login_help()
    elif command == 'new':
        login = input('Write new login> ')
        password = input('Write password> ')
        if not create_login(login, password, parser):
            print('This login is already exist(')
    elif command == 'exit':
        exit_with_question()
    elif command == 'login':
        login = input('Write login> ')
        password = input('Write password> ')
        answer = get_in(login, password, parser)
        if answer:
            print(f'Welcome, {login}!')
            break
        else:
            print('Wrong password or login(')
    else:
        print('Invalid command')


while True:
    command = input('Write the comand> ')
    if command == 'help':
        play_help()
    elif command == 'show':
        tokens = check_tokens(login, parser)
        print(f'You have {tokens} tokens')
    elif command == 'add':
        amount = int(input('How many tokens do you want?'))
        if amount <= 0:
            print('amount is invalid')
        else:
            add_take_tokens(login, amount, parser)
    elif command == 'exit':
        exit()
    elif command == 'play':
        bet = int(input('choose your bet> '))
        colour = str(input('choose your color> '))
        play(login, colour, bet, parser)
    else:
        print('Invalid command')
