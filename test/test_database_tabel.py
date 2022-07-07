import unittest
import telebot
from helpers import database

bot = telebot.TeleBot("5341280498:AAE3ZTwNttnUuVkap6c3YdNavyteAx5xLHs", threaded=False)
database = database.Database("database.db")


class Test_database_tabel(unittest.TestCase):

    def test_nim_terdaftar(self):
        user_message = "/start"
        user_id = 811693737  # user id benar

        def handlestart(message, user_id):
            if (message == '/start'):
                if database.check_user(user_id) == []:
                    return True
                else:
                    return False

        self.assertFalse(handlestart(user_message, user_id))

    def test_nim_tidak_terdaftar(self):
        user_message = "/start"
        user_id = 8116937371  # user id salah

        def handlestart(message, user_id):
            if (message == '/start'):
                if database.check_user(user_id) == []:
                    return True
                else:
                    return False

        self.assertTrue(handlestart(user_message, user_id))

    def test_igracias_tidak_terdaftar(self):
        user_message = "/start"
        user_id = 8116937371

        def handlestart(message, user_id):
            if (message == '/start'):
                if database.check_igracias(user_id) == []:
                    return True
                else:
                    return False

        self.assertTrue(handlestart(user_message, user_id))

    def test_igracias_terdaftar(self):
        user_message = "/start"
        user_id = 811693737

        def handlestart(message, user_id):
            if (message == '/start'):

                if database.check_igracias(user_id) == []:
                    return True
                else:
                    return False

        self.assertFalse(handlestart(user_message, user_id))

    def test_lms_tidak_terdaftar(self):
        user_message = "/start"
        user_id = 8116937371

        def handlestart(message, user_id):
            if (message == '/start'):
                if database.check_lms(user_id) == []:
                    return True
                else:
                    return False

        self.assertTrue(handlestart(user_message, user_id))

    def test_lms_terdaftar(self):
        user_message = "/start"
        user_id = 811693737

        def handlestart(message, user_id):
            if (message == '/start'):
                if database.check_lms(user_id) == []:
                    return True
                else:
                    return False

        self.assertFalse(handlestart(user_message, user_id))