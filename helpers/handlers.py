import os
import re
import schedule
import telebot.types
from src.LmsManager import *
from helpers import database
from helpers import request_collection
import calendar
import locale
from datetime import date, timedelta, datetime
from cryptography.fernet import Fernet
from pyzbar.pyzbar import decode
from PIL import Image
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def keyboard():
    menu = [
        '/start',
        '/jadwalsekarang',
        '/linkmatkul',
        '/listtugas',
        '/notiftugas',
        '/stopnotiftugas',
        '/connected'

    ]

    markup = ReplyKeyboardMarkup(row_width=5, resize_keyboard=True)
    row = [KeyboardButton(x) for x in menu[:5]]
    markup.add(*row)
    row = [KeyboardButton(x) for x in menu[5:7]]
    markup.add(*row)
    markup.add(
        KeyboardButton("✅ Done")
    )
    return markup


def time_greeting():
    now = datetime.now()
    hour = now.hour
    if hour >= 0 and hour < 12:
        return "Selamat Pagi"
    elif hour >= 12 and hour < 18:
        return "Selamat Siang"
    elif hour >= 18 and hour < 24:
        return "Selamat Malam"


class handlers:
    def __init__(self, bot, key):
        self.database = database.Database("database.db")
        self.request = request_collection.requestCollection()
        self.telebot_type = telebot.types.ReplyKeyboardRemove()
        self.bot = bot
        self.key = key

    # handler proses registrasi nim
    def save_nim(self, message):

        try:
            self.bot.clear_step_handler(message)
            chat_id = message.chat.id
            user_id = message.from_user.id
            nim = message.text

            # cek nim ada atau tidak di database
            if self.database.check_nim(nim) == []:
                # jika nim tidak digit atau tidak sama dengan 8 digit
                if not nim.isdigit() or len(nim) != 8:
                    # tampilkan pesan error
                    self.bot.send_message(chat_id, "Nim harus angka dan berjumlah 8 digit",
                                          )
                    self.bot.register_next_step_handler(message, self.save_nim)
                    return

                # jika sukses, simpan nim ke database
                self.database.insert("user", "id_telegram, nim", "{}, '{}'".format(user_id, nim))
                self.bot.send_message(chat_id, "Nim berhasil disimpan !")
                self.bot.send_message(chat_id,
                                      "Dapatkan informasi mengenai Informasi Akademik di Institut Teknologi Telkom Purwokerto dengan menggunakan command /start atau /help\n\n")
            else:
                self.bot.send_message(chat_id,
                                      "Nim sudah terdaftar !\nPastikan NIMmu benar dan coba lagi.\nJika ada kendala lain, hubungi admin bot ini.",
                                      )
        except Exception as e:
            print(e)

    # handler save igracias
    def save_igracias(self, message):
        try:

            chat_id = message.chat.id
            user_id = message.from_user.id
            user_pass = message.text

            if user_pass == "batal":
                self.bot.send_message(chat_id, "Batal Autentikasi IGRACIAS", )
                self.bot.clear_step_handler(message)
                return

            if self.database.check_igracias(user_id) == []:
                if "|" not in user_pass:
                    self.bot.send_message(chat_id,
                                          "Isian harus berformat username|password\nUntuk membatalkan, ketik batal",
                                          )
                    self.bot.register_next_step_handler(message, self.save_igracias)
                    return

                login = self.request.get_link_matkul(
                    username=user_pass.split("|")[0],
                    password=user_pass.split("|")[1],
                    nim=self.database.check_user(user_id)[0][0]
                )
                if login is False:
                    self.bot.send_message(chat_id, "Username atau password salah\nUntuk membatalkan, ketik batal")
                    self.bot.register_next_step_handler(message, self.save_igracias)
                    return
                f = Fernet(self.key)
                encrypted = f.encrypt(user_pass.split("|")[1].encode())
                self.database.insert("igracias_login", "id_telegram, username, password",
                                     "{}, '{}', '{}'".format(user_id, user_pass.split("|")[0], encrypted.decode()))
                self.bot.send_message(chat_id, "Berhasil autentikasi IGRACIAS ITTP WEB")
                self.bot.send_message(chat_id,
                                      "Dapatkan informasi mengenai IGRACIAS ITTP dengan menggunakan command /start atau /help\n\n")
            else:
                self.bot.send_message(chat_id,
                                      "Nim sudah terdaftar !\nPastikan NIMmu benar dan coba lagi.\nJika ada kendala lain, hubungi admin bot ini.",
                                      )
                self.bot.clear_step_handler(message)
                return


        except Exception as e:
            print(e)

    # handler save lms
    def save_lms(self, message):
        try:

            chat_id = message.chat.id
            user_id = message.from_user.id
            user_pass = message.text

            if user_pass == "batal":
                self.bot.send_message(chat_id, "Batal Autentikasi LMS")
                self.bot.clear_step_handler(message)
                return

            # check lms in database
            if self.database.check_lms(user_id)[0][2] is None:
                if "|" not in user_pass:
                    self.bot.send_message(chat_id,
                                          "Isian harus berformat username|password\nUntuk membatalkan, ketik batal",
                                          )
                    self.bot.register_next_step_handler(message, self.save_lms)
                    return
                f = Fernet(self.key)
                encrypted = f.encrypt(user_pass.split("|")[1].encode())
                try:
                    login_lms = LmsManager(
                        username=user_pass.split("|")[0],
                        password=user_pass.split("|")[1],
                    )
                    login_lms.Login()
                except LoginError:
                    self.bot.send_message(chat_id, "Username atau password salah\nUntuk membatalkan, ketik batal",
                                          )
                    self.bot.register_next_step_handler(message, self.save_lms)
                    return

                self.database.update("user", "username_lms", "'{}'".format(user_pass.split("|")[0]), str(user_id))
                self.database.update("user", "password_lms", "'{}'".format(encrypted.decode('utf-8')), str(user_id))
                self.bot.send_message(chat_id, "Berhasil autentikasi LMS")


        except Exception as e:
            print(e)

    # handler untuk command /start
    def start(self, message):
        # cek user_id sudah terdaftar di database atau belum
        user_id = message.from_user.id
        if self.database.check_user(user_id) == []:
            # jika belum, maka lakukan proses registrasi
            self.bot.reply_to(message, "Halo {} !\nKamu baru saja bergabung di bot ini.\n".format(
                message.from_user.first_name))
            self.bot.send_message(message.chat.id,
                                  "Di bot ini kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)

        else:

            if message.text == "✅ Done":
                markup = self.telebot_type
                self.bot.send_message(message.from_user.id, "Done with Keyboard", reply_markup=markup)
                return

            name = message.from_user.first_name if message.from_user.first_name is not None else str(
                message.from_user.id)
            self.bot.reply_to(message,
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
                                                                       "Powered by Extraordinary Team - Kelompok 7",

                              )
            self.bot.send_message(message.chat.id, "Atau bisa menggunakan keyboard berikut:\n\n",
                                  reply_markup=keyboard())

    # handler untuk command /jadwalsekarang
    def get_jadwal_sekarang(self, message):
        print("fungsi get_jadwal_sekarang terpanggil ")
        # check if user is in database
        user_id = message.from_user.id
        if self.database.check_user(user_id) == []:
            self.bot.reply_to(message, "Kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)
            return

        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

        curr_time = datetime.now()
        curr_time = curr_time.strftime("%H:%M")

        curr_date = date.today()
        today = calendar.day_name[curr_date.weekday()]

        nim = self.database.check_user(user_id)[0][0]
        if nim is None:
            self.bot.reply_to(message, "Kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)
            return

        try:

            jadwal = self.request.get_jadwal(nim)
        except Exception as e:
            print(e)
            self.bot.reply_to(message, "Terjadi kesalahan.\nCoba lagi nanti.")
            return

        jadwal_all = ""
        jadwal_list = []
        for i in jadwal:
            if today.upper() in i:
                jadwal_all += i
                jadwal_list.append(i)

        print(jadwal_list)

        jadwal_sekarang = ""
        for i in jadwal_list:
            shift = i.split("\n")[1]
            start = shift.split(" ")[2]
            end = shift.split(" ")[4]
            if start <= curr_time <= end:
                jadwal_sekarang += i
            else:
                jadwal_sekarang += "\nTidak ada jadwal sekarang"

        self.bot.reply_to(message,
                          "Jadwal Kuliah yang berlangsung jam ini :\n\n" + jadwal_sekarang + "\n\n"
                                                                                             "Jadwal Mata Kuliah hari ini:\n\n" + jadwal_all + "\n\n")
        print("[SUCCESS] Get Jadwal Sekarang")

    # handler untuk command /getmatkul
    def get_link_matkul(self, message):
        # check if user is in database
        user_id = message.from_user.id
        if self.database.check_user(user_id) == []:
            self.bot.reply_to(message, "Kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)
            return

        if self.database.check_igracias(user_id) == []:
            self.bot.reply_to(message,
                              "Kamu belum melengkapi Username & Password Igracias .\nSilahkan kirimkan Username & Passwordmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_igracias)
            return

        # get nim from database
        nim = self.database.check_user(user_id)[0][0]
        if nim is None:
            self.bot.reply_to(message, "Kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)
            return

        get_igracias = self.database.check_igracias(user_id)[0]
        f = Fernet(self.key)
        password = f.decrypt(get_igracias[2].encode())
        try:

            link = self.request.get_link_matkul(
                nim=nim,
                username=get_igracias[1],
                password=password.decode('utf-8')
            )
        except TimeoutError:
            self.bot.reply_to(message, "Terjadi kesalahan.\nCoba lagi nanti.")
            return

        tmp = ""
        for i in link.json()['aaData']:
            tmp += "Matkul : " + i[4] + "\nLink : " + i[9] + "\n\n"

        self.bot.reply_to(message, tmp)
        print("[SUCCESS] Get link matkul")

    # handler for get list tugas command
    def get_list_tugas(self, message):
        # check if user is in database
        user_id = message.from_user.id
        if self.database.check_user(user_id) == []:
            self.bot.reply_to(message, "Kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)
            return

        # get nim from database
        nim = self.database.check_user(user_id)[0][0]
        if nim is None:
            self.bot.reply_to(message, "Kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)
            return

        if self.database.check_lms(user_id)[0][2] is None:
            self.bot.reply_to(message,
                              "Kamu belum melengkapi Username & Password LMS.\nSilahkan kirimkan Username & Passwordmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_lms)
            return
        f = Fernet(self.key)
        password = f.decrypt(self.database.check_lms(user_id)[0][3].encode())
        try:
            lmsm = LmsManager(
                username=self.database.check_lms(user_id)[0][2],
                password=password.decode('utf-8'),
            )
            lmsm.Login()
            list_tugas = lmsm.Get_activity(end_time=12)
            tmp = ""
            counter = 1
            for i in list_tugas:
                tmp += "Tugas ke (" + str(counter) + ")\nMatkul : " + i['full_name'] + "\nDeadline : " + i[
                    'deadline'] + "\nTugas : " + i[
                           'name'] + "\n\n"
                counter += 1
            else:
                tmp += "Tidak ada tugas lagi"

            self.bot.reply_to(message, tmp)
            print("[SUCCESS] Get list tugas")

        except Exception as e:
            print(e)
            self.bot.reply_to(message, "Terjadi kesalahan.\nCoba lagi nanti.")
            return

    def gen_markup(self, status=None, id_telegram=None):
        markup = InlineKeyboardMarkup()
        if status == "all_conected":
            markup.row_width = 2
            markup.add(
                InlineKeyboardButton("Unlink All Application", callback_data="unlink_all_app|" + str(id_telegram)),
                InlineKeyboardButton("Cancel", callback_data="cb_no|" + str(id_telegram))
            )

            return markup
        elif status == "lms_not_connected":
            markup.row_width = 2
            markup.add(
                InlineKeyboardButton("Connect LMS", callback_data="connect_lms|" + str(id_telegram)),
                InlineKeyboardButton("Cancel", callback_data="cb_no|" + str(id_telegram))
            )

            return markup
        elif status == "igracias_not_connected":
            markup.row_width = 2
            markup.add(
                InlineKeyboardButton("Connect Igracias", callback_data="connect_igracias|" + str(id_telegram)),
                InlineKeyboardButton("Cancel", callback_data="cb_no|" + str(id_telegram))
            )

            return markup
        elif status == "all_not_connected":
            markup.row_width = 3
            markup.add(
                InlineKeyboardButton("Connect LMS", callback_data="connect_lms|" + str(id_telegram)),
                InlineKeyboardButton("Connect Igracias", callback_data="connect_igracias|" + str(id_telegram)),
                InlineKeyboardButton("Cancel", callback_data="cb_no|" + str(id_telegram))
            )
            return markup

    def callback_query(self, call):
        call_data = call.data.split("|")
        action = call_data[0]
        user_id = call_data[1]

        if action == "unlink_all_app":

            # update to null
            self.database.update("user", "username_lms", "NULL", str(user_id))
            self.database.update("user", "password_lms", "NULL", str(user_id))
            self.database.update("igracias_login", "username", "NULL", str(user_id))
            self.database.update("igracias_login", "password", "NULL", str(user_id))

            self.bot.answer_callback_query(call.id, "All application unlinked")
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
        elif action == "connect_lms":
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.answer_callback_query(call.id, "Please send your username and password")
            self.bot.register_next_step_handler(call.message, self.save_lms)
        elif action == "connect_igracias":
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.answer_callback_query(call.id, "Please send your username and password")
            self.bot.register_next_step_handler(call.message, self.save_igracias)
        elif action == "cb_no":
            self.bot.delete_message(call.message.chat.id, call.message.message_id)
            self.bot.answer_callback_query(call.id, "Canceled")

    # handler for connection lms and igracias
    def get_connected(self, message):

        igracias_connect = False
        lms_connect = False
        global get_igracias

        nim = self.database.check_user(message.from_user.id)[0][0]
        if nim is None:
            self.bot.reply_to(message, "Kamu belum melengkapi NIM.\nSilahkan kirimkan NIMmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_nim)
            return

        if self.database.check_igracias(message.from_user.id) == []:

            self.bot.reply_to(message,
                              "Kamu belum melengkapi Username & Password Igracias .\nSilahkan kirimkan Username & Passwordmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_igracias)

        else:

            get_igracias = self.database.check_igracias(message.from_user.id)[0]
            if get_igracias[1] is None or get_igracias[2] is None:
                self.bot.reply_to(message,
                                  "Kamu belum melengkapi Username & Password Igracias .\nSilahkan kirimkan Username & Passwordmu ke bot ini.")
                self.bot.register_next_step_handler(message, self.save_igracias)
                return
        f = Fernet(self.key)
        password = f.decrypt(get_igracias[2].encode())
        try:

            link = self.request.get_link_matkul(
                nim=nim,
                username=get_igracias[1],
                password=password.decode('utf-8')
            )

            if link is False:
                igracias_connect = False
            else:
                igracias_connect = True

        except TimeoutError:
            self.bot.reply_to(message, "Terjadi kesalahan.\nCoba lagi nanti.")
            return

        if self.database.check_lms(message.from_user.id)[0][2] is None:
            self.bot.reply_to(message,
                              "Kamu belum melengkapi Username & Password LMS.\nSilahkan kirimkan Username & Passwordmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_lms)
            return

        f = Fernet(self.key)
        password = f.decrypt(self.database.check_lms(message.from_user.id)[0][3].encode())

        try:
            lmsm = LmsManager(
                username=self.database.check_lms(message.from_user.id)[0][2],
                password=password.decode('utf-8')
            )
            lmsm.Login()
            lms_connect = True
        except LoginError:
            lms_connect = False
        except Exception as e:
            print(e)
            self.bot.reply_to(message, "Terjadi kesalahan.\nCoba lagi nanti.")
            return

        if igracias_connect and lms_connect:
            self.bot.send_message(message.chat.id,
                                  "Kamu sudah terhubung dengan Igracias dan LMS\nSilahkan pilih menu yang ingin kamu lakukan.",
                                  reply_markup=handlers.gen_markup(status="all_conected",
                                                                   id_telegram=message.from_user.id))
        elif igracias_connect and not lms_connect:
            self.bot.send_message(message.chat.id,
                                  "Kamu sudah terhubung dengan Igracias, tapi tidak terhubung dengan LMS\nSilahkan pilih menu yang ingin kamu lakukan.",
                                  reply_markup=handlers.gen_markup(status="lms_not_connected",
                                                                   id_telegram=message.from_user.id))
        elif not igracias_connect and lms_connect:
            self.bot.send_message(message.chat.id,
                                  "Kamu sudah terhubung dengan LMS, tapi tidak terhubung dengan Igracias\nSilahkan pilih menu yang ingin kamu lakukan.",
                                  reply_markup=handlers.gen_markup(status="igracias_not_connected",
                                                                   id_telegram=message.from_user.id))
        else:
            self.bot.send_message(message.chat.id,
                                  "Kamu belum terhubung dengan Igracias dan LMS\nSilahkan pilih menu yang ingin kamu lakukan.",
                                  reply_markup=handlers.gen_markup(status="all_not_conected",
                                                                   id_telegram=message.from_user.id))

    # handler for send_notif
    def send_notif(self, chat_id, user_id):
        print("~ Mengirim notif tugas ke {}".format(chat_id))
        f = Fernet(self.key)
        password = f.decrypt(self.database.check_lms(user_id)[0][3].encode())
        try:
            lmsm = LmsManager(
                username=self.database.check_lms(user_id)[0][2],
                password=password.decode('utf-8'),
            )
            lmsm.Login()
            list_tugas = lmsm.Get_activity(end_time=12)
            tmp = ""
            counter = 1
            for i in list_tugas:
                tmp += "Tugas ke (" + str(counter) + ")\nMatkul : " + i['full_name'] + "\nDeadline : " + i[
                    'deadline'] + "\nTugas : " + i[
                           'name'] + "\n\n"
                counter += 1
            else:
                tmp += "Tidak ada tugas lagi"
        except LoginError:
            tmp = "Login Error"

        self.bot.send_message(chat_id, "Notif Tugas !\n\n" + tmp + "\n\nJangan lupa mengerjakan yaa")

    # handler for get notif
    def get_notiftugas(self, message):
        if self.database.check_lms(message.from_user.id)[0][2] is None:
            self.bot.reply_to(message,
                              "Kamu belum melengkapi Username & Password LMS.\nSilahkan kirimkan Username & Passwordmu ke bot ini.")
            self.bot.register_next_step_handler(message, self.save_lms)
            return

        user_id = message.from_user.id

        print("~  USER ID : " + str(message.from_user.id) + " Mengaktifkan Notif Tugas")

        all_jobs = schedule.get_jobs(user_id)
        if len(all_jobs) <= 0:
            # Check Databse

            if self.database.check_notif_tugas(user_id) == []:
                self.database.insert("schedule_task", "message_chat_id, user_id, last_status, id_telegram",
                                     "{}, '{}', '{}', '{}'".format(message.chat.id, user_id, str(1),
                                                                   str(message.from_user.id)))
            else:
                self.database.update("schedule_task", "last_status", str(1), str(user_id))

            self.bot.send_message(message.chat.id,
                                  "Fitur Notif Tugas diaktifkan\nNotif akan dikirim setiap 3 jam sekali\nuntuk menonaktifkan fitur ini, ketik /stopnotiftugas")
            schedule.every(3).hours.do(self.send_notif, chat_id=message.chat.id, user_id=user_id).tag(message.chat.id)
        else:
            self.database.update("schedule_task", "last_status", str(0), str(user_id))
            self.bot.send_message(message.chat.id,
                                  "Fitur Notif tugas telah dinonaktifkan\nUntuk mengaktifkan kembali fitur ini, ketik /notiftugas")

            schedule.clear(user_id)

    def unset_timer(self, message):
        user_id = message.from_user.id
        self.database.update("schedule_task", "last_status", str(0), str(user_id))
        schedule.clear(message.chat.id)
        self.bot.send_message(message.chat.id, "Notif Tugas telah dihentikan")
