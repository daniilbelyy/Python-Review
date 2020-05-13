import argparse
import requests

def create_main_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', default='localhost')
    parser.add_argument('port', default=8000)
    return parser.parse_args()
def get_in(login, password, parser):
    return bool(requests.get(f'http://{parser.host}:{parser.port}/autification', dict(login = login, password = password)).text)

def create_login(login, password, parser):
    return bool(requests.post(f'http://{parser.host}:{parser.port}/autification', dict(login = login, password = password)).text)

def check_tokens(username, parser):
    return (requests.get(f'http://{parser.host}:{parser.port}/{username}/tokens').text)

def add_take_tokens(username, amount, parser):
    return bool(requests.post(f'http://{parser.host}:{parser.port}/{username}/tokens', amount).text)

def play(username, colour, bet, parser):
    if add_take_tokens(username, -bet, parser):
        tokens = check_tokens(username, parser)
        print(f'Your tokens for now: {tokens}') 
        result = list(requests.get(f'http://{parser.host}:{parser.port}/{username}/game').text)
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
        add_take_tokens(username, bet, parser)
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
while True:
    command = input('Write the comand> ')
    if command == 'help':
        login_help()
    elif command == 'new':
        login = input('Write new login> ')
        password = input('Write password> ')
        create_login(login, password, parser)
    elif command == 'exit':
        exit()
    elif command == 'login':
        login = input('Write login> ')
        password = input('Write password> ')
        answer = get_in(login, password, parser)
        if answer:
            print(f'Welcome, {login}!')
            break
        else:
            print('Wrong password(')
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
        colour = chr(input('choose your color> '))
        play(login, colour, bet, parser)
    else:
        print('Invalid command')                