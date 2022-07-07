import unittest
import telebot
from helpers import database, request_collection

bot = telebot.TeleBot("5341280498:AAE3ZTwNttnUuVkap6c3YdNavyteAx5xLHs", threaded=False)
database = database.Database("database.db")
request = request_collection.requestCollection()

class Test_handler_linkmatkul(unittest.TestCase):

    def test_linkmatkul_salah(self):
        user_message = "/linkmatkul"
        user_id = 811693737
        nim = "21104059"
        username = "@test"
        password = "test"

        def handlelinkmatkul(message, user_id):
            if (message == '/linkmatkul'):

                request_get_link = request.get_link_matkul(username, password, nim)
                print(request_get_link)
                if request_get_link is False:
                    return True
                else:
                    return False

        self.assertTrue(handlelinkmatkul(user_message, user_id))


    def test_linkmatkul_benar(self):
        user_message = "/linkmatkul"
        user_id = 811693737
        nim = "21104059"
        username = ""
        password = ""

        def handlelinkmatkul(message, user_id):
            if (message == '/linkmatkul'):

                request_get_link = request.get_link_matkul(username, password, nim)
                print(request_get_link)
                if request_get_link is True:
                    return True
                else:
                    return False

        self.assertFalse(handlelinkmatkul(user_message, user_id))


