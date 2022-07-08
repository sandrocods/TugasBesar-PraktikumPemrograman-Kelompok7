##
# Author  : Sandroputraa
# Name    : Igracias LMS ITTP Telegram Bot
# Build   : 08-07-2022
#
# If you are a reliable programmer or the best developer, please don't change anything.
# If you want to be appreciated by others, then don't change anything in this script.
# Please respect me for making this tool from the beginning.
##

# Import Module yang dibutuhkan
import telebot
import ascii_magic
import time, threading, schedule
from datetime import datetime
from colorama import Fore, init
from helpers import handlers, database

# Inisialisasi Colorama untuk menampilkan output autoreset
init(autoreset=True)

# Fernet Key Token
key = "pY_Gd91tWcO5Df6eVlW8JpzKYGrb2vnUOfjucwGzUoo="

# Menampilkan logo ITTP
img = ascii_magic.from_image_file("logo_ittp.png", columns=45, width_ratio=2.5)
result = ascii_magic.to_terminal(img)
print(Fore.RED + "          IGRACIAS ITTP TELEGRAM BOT")

# Membuat object Telebot yang ditampung dalam variabel bot
# parameter token = TOKEN,  dari bot father
# parameter parse_mode = HTML, untuk mengubah format teks menjadi HTML
# parameter threaded = True, untuk menjalankan bot dalam thread
# parameter num_threads = int(2), untuk mengatur jumlah thread
bot = telebot.TeleBot(
    token="",
    parse_mode="HTML",
    threaded=True,
    num_threads=int(2)
)

# Membuat instance class handlers yang ditampung dalam variabel handlers
# parameter bot = bot, dari bot father
# parameter key = key, dari Fernet Key Token
handlers = handlers.handlers(bot, key)

# Membuat instance class database yang ditampung dalam variabel database
# parameter database = "database.db", nama database
database = database.Database("database.db")

try:
    # Cek koneksi database
    try:
        database.check_connection()

    except Exception as e:
        print(Fore.RED + "Database Connection Error: " + str(e))
        exit()

    print(Fore.GREEN + "Starting Bot 🚀 ...")


    #
    # Handler yang akan dijalankan saat ada pesan dari user
    #

    # handler /start
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        print(Fore.GREEN + "[" + str(datetime.now()) + "] " + Fore.RESET + "Pesan Baru Dari : " + str(
            message.from_user.id) + " " + Fore.LIGHTYELLOW_EX + " Aksi : Start" + Fore.RESET)
        handlers.start(message)


    # Handle /jadwalsekarang
    @bot.message_handler(commands=['jadwalsekarang'])
    def get_jadwal_sekarang(message):
        print(Fore.GREEN + "[" + str(datetime.now()) + "] " + Fore.RESET + "New message from : " + str(
            message.from_user.id) + " " + Fore.LIGHTYELLOW_EX + " Action : Get Jadwal Sekarang" + Fore.RESET)
        handlers.get_jadwal_sekarang(message)


    # Handle /linkmatkul
    @bot.message_handler(commands=['linkmatkul'])
    def get_link_matkul(message):
        print(Fore.GREEN + "[" + str(datetime.now()) + "] " + Fore.RESET + "New message from : " + str(
            message.from_user.id) + " " + Fore.LIGHTYELLOW_EX + " Action : Get Link Matkul" + Fore.RESET)
        handlers.get_link_matkul(message)


    # Handle /listtugas
    @bot.message_handler(commands=['listtugas'])
    def get_list_tugas(message):
        print(Fore.GREEN + "[" + str(datetime.now()) + "] " + Fore.RESET + "New message from : " + str(
            message.from_user.id) + " " + Fore.LIGHTYELLOW_EX + " Action : Get List Tugas" + Fore.RESET)
        handlers.get_list_tugas(message)


    # Handle /connected
    @bot.message_handler(commands=['connected'])
    def get_connected(message):
        print(Fore.GREEN + "[" + str(datetime.now()) + "] " + Fore.RESET + "New message from : " + str(
            message.from_user.id) + " " + Fore.LIGHTYELLOW_EX + " Action : Get Connected" + Fore.RESET)
        handlers.get_connected(message)


    # Handle /notiftugas
    @bot.message_handler(commands=['notiftugas'])
    def get_notif_tugas(message):
        print(Fore.GREEN + "[" + str(datetime.now()) + "] " + Fore.RESET + "New message from : " + str(
            message.from_user.id) + " " + Fore.LIGHTYELLOW_EX + " Action : Get Notif Tugas" + Fore.RESET)
        handlers.get_notiftugas(message)


    # Handle /stopnotiftugas
    @bot.message_handler(commands=['stopnotiftugas'])
    def unset_timer(message):
        print(Fore.GREEN + "[" + str(datetime.now()) + "] " + Fore.RESET + "New message from : " + str(
            message.from_user.id) + " " + Fore.LIGHTYELLOW_EX + " Action : Stop Notif Tugas" + Fore.RESET)
        handlers.unset_timer(message)


    threading.Thread(target=bot.infinity_polling, name='bot_infinity_polling', daemon=True).start()
    while True:
        schedule.run_pending()
        time.sleep(1)


except Exception as e:
    print(Fore.RED + "Error: " + str(e))
    exit()
