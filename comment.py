import time


class Comment:
    def __init__(self, mid, username, gender, ctime,
                 content, likes, rcount, rpid):
        self.mid = mid
        self.rpid = rpid
        self.username = username
        self.gender = gender
        self.ctime = time.strftime("%Y-%m-%d %H:%M:%S",
                                   time.localtime(ctime))
        self.content = content
        self.likes = likes
        self.rcount = rcount
