import unittest
import telebot
from helpers import database
from datetime import date, timedelta, datetime

bot = telebot.TeleBot("5341280498:AAE3ZTwNttnUuVkap6c3YdNavyteAx5xLHs", threaded=False)
database = database.Database("database.db")

class Test_handler_start(unittest.TestCase):

    def test_start_terdaftar(self):
        user_message = "/start"
        user_id = 811693737
        name = "test"

        def time_greeting():
            now = datetime.now()
            hour = now.hour
            if hour >= 0 and hour < 12:
                return "Selamat Pagi"
            elif hour >= 12 and hour < 18:
                return "Selamat Siang"
            elif hour >= 18 and hour < 24:
                return "Selamat Malam"

        def handlestart(message, user_id):
            if (message == '/start'):
                if database.check_user(user_id) == []:
                    bot.send_message(user_id, "Selamat datang di Igracias, silahkan isi data diri anda")
                    return True
                else:
                    bot.send_message(user_id, "Halo " + time_greeting() + " " + name + "\nSelamat Datang di Media Informasi Akademik Institut Teknologi Telkom Purwokerto 🙌"
                                                                       "\nDapatkan informasi akademik dengan menggunakan command dibawah\n\n\n"

                                                                       "🗓 Menu Jadwal \n"
                                                                       "/jadwalsekarang - Untuk melihat jadwal Mata Kuliah yang sedang berlangsung\n"
                                                                       "/linkmatkul - Untuk melihat link matakuliah\n\n\n"


                                                                       "📚 Menu Tugas \n"
                                                                       "/listtugas - Untuk melihat semua tugas yang belum selesai\n"
                                                                       "/notiftugas - Untuk memberikan notifikasi tugasmu yang belum selesai\n"
                                                                       "/stopnotiftugas - Untuk menghentikan notifikasi tugasmu yang belum selesai\n\n"

                                                                       "⚙️ Menu Setting \n"
                                                                       "/connected - Untuk melihat aplikasi yang terhubung\n\n\n"
                                                                       "Powered by Extraordinary Team - Kelompok 7",)
                    return False

        self.assertFalse(handlestart(user_message, user_id))

    def test_start_tidak_terdaftar(self):

        user_message = "/start"
        user_id = 1498919525
        name = "test"

        def time_greeting():
            now = datetime.now()
            hour = now.hour
            if hour >= 0 and hour < 12:
                return "Selamat Pagi"
            elif hour >= 12 and hour < 18:
                return "Selamat Siang"
            elif hour >= 18 and hour < 24:
                return "Selamat Malam"

        def handlestart(message, user_id):
            if (message == '/start'):
                if database.check_user(user_id) == []:
                    bot.send_message(user_id, "Selamat datang di Igracias, silahkan isi data diri anda")
                    return True
                else:
                    bot.send_message(user_id,
                                     "Halo " + time_greeting() + " " + name + "\nSelamat Datang di Media Informasi Akademik Institut Teknologi Telkom Purwokerto 🙌"
                                                                              "\nDapatkan informasi akademik dengan menggunakan command dibawah\n\n\n"

                                                                              "🗓 Menu Jadwal \n"
                                                                              "/jadwalsekarang - Untuk melihat jadwal Mata Kuliah yang sedang berlangsung\n"
                                                                              "/linkmatkul - Untuk melihat link matakuliah\n\n\n"


                                                                              "📚 Menu Tugas \n"
                                                                              "/listtugas - Untuk melihat semua tugas yang belum selesai\n"
                                                                              "/notiftugas - Untuk memberikan notifikasi tugasmu yang belum selesai\n"
                                                                              "/stopnotiftugas - Untuk menghentikan notifikasi tugasmu yang belum selesai\n\n"

                                                                              "⚙️ Menu Setting \n"
                                                                              "/connected - Untuk melihat aplikasi yang terhubung\n\n\n"
                                                                              "Powered by Extraordinary Team - Kelompok 7", )
                    return False

        self.assertTrue(handlestart(user_message, user_id))