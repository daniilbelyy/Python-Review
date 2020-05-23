import unittest
import library

class TestCassino(unittest.TestCase):
    def test_add_user_1(self):
        login = 'login'
        password = 'password'
        user_passwords = dict()
        tokens = dict()
        library.add_user(user_passwords, tokens, login, password)
        self.assertEqual(user_passwords[login], 'password')

    def test_add_user_2(self):
        login = 'login'
        password = 'password_1'
        tokens = dict()
        user_passwords = dict(login = 'password')
        library.add_user(user_passwords, tokens, login, password)
        self.assertEqual(user_passwords[login], 'password')

    def test_check_passwords_1(self):
        login = 'login'
        password = 'password'
        user_passwords = dict(login = 'password')
        result = library.check_passwords(user_passwords, login, password)
        self.assertEqual(result, True)

    def test_check_passwords_2(self):
        login = 'login'
        password = 'password1'
        user_passwords = dict(login = 'password')
        result = library.check_passwords(user_passwords, login, password)
        self.assertEqual(result, False)

    def test_add_tokens(self):
        login = 'login'
        tokens = dict(login = 0)
        amount = 100
        library.add_tokens(login, tokens, amount)
        self.assertEqual(tokens[login], 100)

    def test_check_tokens(self):
        tokens = dict(login = 100)
        answer = library.check_tokens('login', tokens)
        self.assertEqual(answer, 100)
