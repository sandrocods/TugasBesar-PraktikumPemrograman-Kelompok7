import unittest
import telebot
from helpers import database, request_collection

bot = telebot.TeleBot("5341280498:AAE3ZTwNttnUuVkap6c3YdNavyteAx5xLHs", threaded=False)
database = database.Database("database.db")
request = request_collection.requestCollection()

class Test_handler_jadwalsekarang(unittest.TestCase):

    def test_jadwalsekarang_benar(self):
        user_message = "/jadwalsekarang"
        user_id = 811693737
        nim = "21104059" # nim benar

        def handlejadwalsekarang(message, user_id):
            if (message == '/jadwalsekarang'):

                request_get_jadwal = request.get_jadwal(nim)
                print(request_get_jadwal)
                if request_get_jadwal is not None:
                    return True
                else:
                    return False

        self.assertTrue(handlejadwalsekarang(user_message, user_id))

    def test_jadwalsekarang_salah(self):
        user_message = "/jadwalsekarang"
        user_id = 811693737
        nim = "211040591"

        def handlejadwalsekarang(message, user_id):
            if (message == '/jadwalsekarang'):

                request_get_jadwal = request.get_jadwal(nim)
                print(request_get_jadwal)
                if request_get_jadwal is not None:
                    return False
                else:
                    return True
        self.assertFalse(handlejadwalsekarang(user_message, user_id))
