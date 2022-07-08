##
# Author  : Sandroputraa
# Name    : Igracias LMS ITTP Telegram Bot
# Build   : 08-07-2022
#
# If you are a reliable programmer or the best developer, please don't change anything.
# If you want to be appreciated by others, then don't change anything in this script.
# Please respect me for making this tool from the beginning.
##

class LoginError(Exception):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        super().__init__(f"Username : {self.username} & Password : {self.password} inccorect")


class GetActivityError(Exception):
    def __init__(self):
        super().__init__(f"Failed Get Activity")


class CookieExpire(Exception):
    def __init__(self):
        super().__init__(f"Cookie Expire Login Again")


class SendNotification(Exception):
    def __init__(self):
        super().__init__(f"Bot Token and Chat ID can't None")
