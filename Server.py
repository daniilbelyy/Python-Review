import flask 
import argparse
import random
import Library
import pages

app = flask.Flask('Cassino')


def create_main_parser(defaulthost, defaultport):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default=defaulthost)
    parser.add_argument('--port', default= defaultport)
    return parser.parse_args()


@app.route('/{autification_page}', methods=['POST'])
def create_login():
    login = str(flask.request.args['login'])
    password = str(flask.request.args['password'])
    return library.add_user(users_passwords, tokens, login, password)


@app.route('/{autification_page}', methods=['GET'])
def log_in():
    login = str(flask.request.args['login'])
    password = str(flask.request.args['password'])
    return library.check_password(users_passwords, login, password)


@app.route('/<username>/{tokens_page}', methods=['POST'])
def add_take_tokens(username):
    amount = int(flask.request.args['amount'])
    if tokens[username] + amount >= 0:
        return library.add_tokens(username, tokens, amount)
    else:
        return False


@app.route('/<username>/{tokens_page}', methods=['GET'])
def check_amount_of_tokens(username):
    return str(library.check_tokens(username, tokens))


@app.route('/<username>/{game_page}', methods=['GET'])
def play(usernamem, red_spots, black_spots, green_spots):
    all_colours = len(red_spots) + len(black_spots) + len(green_spots)
    score = random.randint(1, all_colours)
    if score in red_spots:
        return f'red {score}'
    if score in black_spots:
        return f'black {score}'
    if score in green_spots:
        return f'green {score}'


def main():
    parser = create_main_parser()
    users_passwords = {}
    tokens = {}

    app.run(parser.host, parser.port, debug=True, use_reloader = False)


defaulthost = localhost
defaultport = 8000
red_spots = [1, 3, 5, 7, 9, 11, 13]
black_spots = [2, 4, 6, 8, 10, 12, 14]
green_spots = [15]


if __name__ == '__main__':
    main()
