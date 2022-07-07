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
