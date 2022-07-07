import unittest
import telebot
from helpers import database
from src.LmsManager import LmsManager

bot = telebot.TeleBot("5341280498:AAE3ZTwNttnUuVkap6c3YdNavyteAx5xLHs", threaded=False)
database = database.Database("database.db")


class Test_handler_listtugas(unittest.TestCase):

    def test_list_tugas_benar(self):
        user_message = "/listtugas"
        user_id = 811693737
        nim = "21104059"
        username = ""
        password = ""

        def handlelisttugas(message, user_id):
            if (message == '/listtugas'):

                request_get_tugas = LmsManager(username=username, password=password)
                request_get_tugas.Login()

                data = request_get_tugas.Get_activity(end_time=30)
                print(data)

                if request_get_tugas is not None:
                    return True
                else:
                    return False
        self.assertTrue(handlelisttugas(user_message, user_id))

    def test_list_tugas_salah(self):
        user_message = "/listtugas"
        user_id = 811693737
        nim = "211040591"
        username = "211040591"
        password = "Sandroxxx132"

        def handlelisttugas(message, user_id):
            if (message == '/listtugas'):

                try:
                    request_get_tugas = LmsManager(username=username, password=password)
                    request_get_tugas.Login()
                    data = request_get_tugas.Get_activity(end_time=30)
                    print(data)
                    return True

                except Exception as e:
                    print(e)
                    return False




        self.assertFalse(handlelisttugas(user_message, user_id))