##
# Author  : Sandroputraa
# Name    : Igracias LMS ITTP Telegram Bot
# Build   : 08-07-2022
#
# If you are a reliable programmer or the best developer, please don't change anything.
# If you want to be appreciated by others, then don't change anything in this script.
# Please respect me for making this tool from the beginning.
##

import re
import json
import time
import requests
import humanize
from src.Exception import *
from os.path import exists
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()
humanize.i18n.activate("id_ID")
endPoint = "https://lms.ittelkom-pwt.ac.id/"


class LmsManager:

    def __init__(self, username, password):

        self.chat_id = None
        self.bot_token = None
        self.id_user = None
        self.headers = None
        self.login_name = None
        self.sesskey = None
        self.moodle_session = None
        self.username = username
        self.password = password

        if not (self.username and self.password):
            raise LoginError(self.username, self.password)

        if not exists("./Cookie/" + self.username + "_cookie.json"):
            with open("./Cookie/" + self.username + "_cookie.json", "w") as save:
                save.write(
                    json.dumps(
                        {
                            "username": self.username,
                            "password": self.password
                        }, indent=2)
                )
            LmsManager.Login(self)

    def sendActivityToTelegram(self):
        """
        It gets the activity of the user and sends it to the telegram bot
        """
        build_message = ""
        getActivity = self.Get_activity(
            end_time=30
        )
        for i in range(len(getActivity)):
            build_message += "Task Number : {task_number}\n\n" \
                             "Lesson Name : {lession_name}\n" \
                             "Task Name : {task_name}\n" \
                             "Deadline : {deadline}\n".format(
                task_number=i,
                lession_name=getActivity[i]['full_name'],
                task_name=getActivity[i]['name'],
                deadline=getActivity[i]['deadline']
            )
        self.send_notification(
            bot_token=self.bot_token,
            chat_id=self.chat_id,
            message=build_message
        )
        del build_message

    def ScheduleTask(self, time_exec=10, bot_token=None, chat_id=None):
        """
        It schedules a task to be executed every 10 seconds.

        :param time_exec: The time interval in seconds between each notification, defaults to 10 (optional)
        :param bot_token: The token of the bot you created
        :param chat_id: The chat id of the telegram channel you want to send the message to
        """

        self.bot_token = bot_token
        self.chat_id = chat_id

        if not (chat_id and bot_token):
            raise SendNotification

        scheduler.add_job(
            func=self.sendActivityToTelegram,
            trigger='interval',
            seconds=time_exec,
            id="schedule_send_task"
        )
        scheduler.start()

    @staticmethod
    def send_notification(bot_token, chat_id, message):
        """
        The above function sends a message to a telegram user.

        :param bot_token: The token of the bot you created
        :param chat_id: The chat ID of the chat you want to send the message to
        :param message: The message you want to send
        :return: A dictionary with two keys: status and msg.
        """
        request_send_message = requests.post(
            url="https://api.telegram.org/bot" + str(bot_token) + "/sendMessage",
            data={'chat_id': chat_id, 'text': message}
        )
        if request_send_message.json()['ok']:
            return {
                'status': True,
                'msg': 'Success Send Message'
            }
        else:
            return {
                'status': False,
                'msg': 'Failed Send Message'
            }

    def Save_cookie(self):
        """
        It saves the user's cookie to a file
        """
        with open("./Cookie/" + self.username + "_cookie.json", "w") as save:
            save.write(
                json.dumps(
                    {
                        "username": self.username,
                        "login_name": self.login_name,
                        "sesskey": self.sesskey,
                        "moodle_session": self.moodle_session,
                        "id_user": self.id_user
                    }, indent=5)
            )

    def check_cookie(self):
        """
        If the file exists, open it and load the json object, then assign the moodle_session value to the variable
        self.moodle_session, then create a header with the moodle_session value, then check if the user is still active by
        sending a request to the endpoint, if the user is not active, raise the CookieExpire exception
        """
        try:
            if exists("./Cookie/" + self.username + "_cookie.json"):
                with open('./Cookie/' + self.username + '_cookie.json', 'r') as openfile:
                    json_object = json.load(openfile)

                self.moodle_session = json_object['moodle_session']

                headers = {
                    "Host": "lms.ittelkom-pwt.ac.id",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Origin": "https://lms.ittelkom-pwt.ac.id",
                    "Content-Type": "application/x-www-form-urlencoded",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                    "Referer": "https://lms.ittelkom-pwt.ac.id/",
                    "Cookie": f"MoodleSession={self.moodle_session}"
                }
                check_active_user = requests.get(url=endPoint + "my/", headers=headers)
                if "Forgotten" in check_active_user.text:
                    raise CookieExpire
                else:
                    pass
        except json.JSONDecodeError:
            raise CookieExpire

    def __process_login(self):
        """
        The above function is a function to login to the moodle website.
        """
        get_login = requests.get(url=endPoint)
        login_token = \
            re.findall(pattern='<input type="hidden" name="logintoken" value="(.*?)" />',
                       string=get_login.text)[0]
        headers = {
            "Host": "lms.ittelkom-pwt.ac.id",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Origin": "https://lms.ittelkom-pwt.ac.id",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Referer": "https://lms.ittelkom-pwt.ac.id/",
            "Cookie": f"MoodleSession={get_login.cookies.get_dict()['MoodleSession']}"
        }
        login = requests.post(url=endPoint + "login/index.php",
                              data=f"logintoken={login_token}&username={self.username}&password={self.password}",
                              headers=headers,
                              allow_redirects=False
                              )
        if not login.cookies.get_dict():
            raise LoginError(self.username, self.password)
        else:
            del headers['Cookie']
            headers['Cookie'] = 'MoodleSession=' + login.cookies.get_dict()['MoodleSession']

            push_session = requests.get(url=login.headers['Location'], headers=headers,
                                        allow_redirects=False)

            main_dashbord = requests.get(url=push_session.headers['Location'], headers=headers)
            try:
                self.moodle_session = login.cookies.get_dict()['MoodleSession']
                self.sesskey = re.findall(
                    pattern='<input type="hidden" name="sesskey" value="(.*?)">',
                    string=main_dashbord.text)[0]
                self.login_name = re.findall(
                    pattern='<span class="usertext mr-1">(.*?)</span>',
                    string=main_dashbord.text)[0]

                self.headers = headers
                self.id_user = re.findall(pattern="testsession=(\d+)", string=login.headers['Location'])[0]
                self.Save_cookie()
            except IndexError:
                raise LoginError(self.username, self.password)

    def Login(self):
        """
        The above function is a function to login to the moodle website.
        :return: The return value is a dictionary with the following keys:
            error: Boolean value, True if there is an error, False if there is no error.
            login_name: String value, the name of the user who logged in.
            sesskey: String value, the session key of the user who logged in.
            moodle_session: String value, the
        """

        if exists("./Cookie/" + self.username + "_cookie.json"):
            with open('./Cookie/' + self.username + '_cookie.json', 'r') as openfile:

                try:
                    json_object = json.load(openfile)
                    self.moodle_session = json_object['moodle_session']
                    self.sesskey = json_object['sesskey']
                    self.headers = {
                        "Host": "lms.ittelkom-pwt.ac.id",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1",
                        "Origin": "https://lms.ittelkom-pwt.ac.id",
                        "Content-Type": "application/x-www-form-urlencoded",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Referer": "https://lms.ittelkom-pwt.ac.id/",
                        "Cookie": f"MoodleSession={self.moodle_session}"
                    }

                    try:
                        self.check_cookie()
                    except CookieExpire:
                        self.__process_login()

                except KeyError:
                    self.__process_login()
                except json.JSONDecodeError:
                    self.__process_login()
        else:
            with open('./Cookie/' + self.username + '_cookie.json', 'r') as openfile:
                json_object = json.load(openfile)
            self.username = json_object['username']
            self.password = json_object['password']

            LmsManager.__process_login(self)

    def Get_activity(self, end_time=6):
        """
        The above function is used to get the activity of the user.
        :return: A list of dictionaries.
        """

        try:
            self.check_cookie()
            try:
                data_activity = []
                current_ts = datetime.now()
                end_ts = current_ts + timedelta(days=end_time)

                get_activity = requests.post(
                    url=endPoint + f"lib/ajax/service.php?sesskey={self.sesskey}&info=core_calendar_get_action_events_by_timesort",
                    data='[{"index":0,"methodname":"core_calendar_get_action_events_by_timesort","args":{"limitnum":26,"timesortfrom":' +
                         str(current_ts.timestamp()).split('.')[0] + ',"timesortto":' +
                         str(end_ts.timestamp()).split('.')[0] + ',"limittononsuspendedevents":true}}]',
                    headers=self.headers
                )

                json_decode = get_activity.json()
                if not json_decode[0]['error']:
                    for data in json_decode[0]['data']['events']:
                        data_activity.append({
                            'id': data['instance'],
                            'full_name': data['course']['fullnamedisplay'],
                            'name': data['name'],
                            'deadline': datetime.fromtimestamp(data['timeusermidnight']).strftime('%d-%m-%y %H:%M:%S'),
                            'deadline_timestamp': datetime.fromtimestamp(data['timeusermidnight'])
                        })
                    return data_activity
                else:
                    raise GetActivityError
            except ConnectionRefusedError:
                time.sleep(2)
                raise GetActivityError
            except ConnectionError:
                time.sleep(2)
                raise GetActivityError
        except CookieExpire:
            raise CookieExpire

    def get_course(self):
        try:
            self.check_cookie()
            try:
                course_list = []
                get_course = requests.post(
                    url=endPoint + f"lib/ajax/service.php?sesskey={self.sesskey}&info=core_course_get_enrolled_courses_by_timeline_classification",
                    data='[{"index":0,"methodname":"core_course_get_enrolled_courses_by_timeline_classification","args":{"offset":0,"limit":0,"classification":"all","sort":"shortname","customfieldname":"","customfieldvalue":""}}]',
                    headers=self.headers
                )

                json_decode = get_course.json()
                if not json_decode[0]['error']:
                    for data in json_decode[0]['data']['courses']:
                        course_list.append({
                            'full_name': data['fullnamedisplay'],
                        })
                    return course_list
                else:
                    raise GetActivityError

            except ConnectionRefusedError:
                time.sleep(2)
                raise GetActivityError
            except ConnectionError:
                time.sleep(2)
                raise GetActivityError
        except CookieExpire:
            raise CookieExpire

    def get_profile(self):
        """
        It gets the profile of the user and returns a dictionary with the full name, email, first access and last access of
        the user
        :return: A dictionary with the user's full name, email, first access, and last access.
        """
        try:
            self.check_cookie()
            try:

                get_profile = requests.get(url=endPoint + f"user/profile.php?id={self.id_user}", headers=self.headers)
                parse = BeautifulSoup(get_profile.text, 'html.parser')
                if not parse.find('h1').text:
                    raise GetActivityError
                else:
                    return {
                        'full_name': parse.find('h1').text,
                        'email': parse.find('dd').findNext('a').text,
                        'first_access': parse.find('li', {"class": "contentnode"}).findNext('dt',
                                                                                            text='First access to site').findNext(
                            'dd').text,
                        'last_access': parse.find('li', {"class": "contentnode"}).findNext('dt',
                                                                                           text='Last access to site').findNext(
                            'dd').text
                    }
            except ConnectionRefusedError:
                time.sleep(2)
                raise GetActivityError
            except ConnectionError:
                time.sleep(2)
                raise GetActivityError

        except CookieExpire:
            raise CookieExpire

    def view_assign(self, id_assign):
        try:
            self.check_cookie()
            try:

                get_profile = requests.get(url=endPoint + f"mod/assign/view.php?id={id_assign}&action=editsubmission",
                                           headers=self.headers)
                parse = BeautifulSoup(get_profile.text, 'html.parser')
                if not parse.find('input', id='id_files_filemanager')['value']:
                    raise GetActivityError

                return {
                    'id_file_manager': parse.find('input', id='id_files_filemanager')['value'],
                    'ctx_id': re.search(r"\"contextid\":(.*?),", get_profile.text).group(1),
                }
            except ConnectionRefusedError:
                time.sleep(2)
                raise GetActivityError
            except ConnectionError:
                time.sleep(2)
                raise GetActivityError

        except CookieExpire:
            raise CookieExpire
