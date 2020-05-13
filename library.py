def add_user(users_passwords, tokens, login, password):
    if not login in users_passwords:
        users_passwords[login] = password
        tokens[login] = 0
        return True
    else:
        return False

def check_password(users_passwords, login, password):
    if users_passwords.get(login) == password:
        return True
    else:
        return False
    
def add_tokens(username, tokens, amount):
    tokens[username] = tokens[username] + amount
    return True

def check_tokens(username, tokens):
    return tokens[username]