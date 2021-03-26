import redis
import sys

class Chat:
    GROUPS = 'GROUPS'
    USERS = 'users'

    def __init__(self, ip, port):
        self.r = redis.Redis(host=ip, port=port, db=0)
        print(self.r)

    def set(self, key, val):
        return self.r.set(key, val)

    def get(self, key):
        return self.r.get(key)

    def get_groups(self):
        """
        Get all available groups to join.
        """
        return self.r.zrange(chat.GROUPS, 0, -1)

class User:
    """
    Each user has its own group with a name thats equal to the
    name of the user.
    """
    def __init__(self, uname, status, chat):
        self.uname = uname
        self.status = status
        self.chat = chat

        # Insert user into db
        self.chat.r.hset("{}:{}".format(chat.USERS, uname), 'uname', uname)
        self.chat.r.hset("{}:{}".format(chat.USERS, uname), 'status', status)
        self.chat.r.zadd(chat.GROUPS, { uname : 1.0 })

        # Enter pub/ sub and subscribe to own channel
        self.channel = chat.r.pubsub()
        self.channel.subscribe(uname)

    def get_message(self):
        msg = self.channel.get_message()
        if msg:
            return msg['data']

    def send_message(self, dst, msg):
        return self.chat.r.publish(dst, "{}\n--------------------\n{}".format(msg, self.status))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: ./chat username <status text>")
        sys.exit(1)

    chat = Chat('localhost', 6379)
    user = User(sys.argv[1], sys.argv[2], chat)

    while(True):
        cmd = input()
        t = cmd.split(' ', 2)

        if t[0] == 'send':
            user.send_message(t[1], t[2])
        elif t[0] == 'get':
            while True:
                message = user.get_message()
                if message == 1 or message == None:
                    break;
                print(message.decode('utf-8'))
        elif t[0] == 'getgroups':
            groups = user.chat.get_groups()
            for group in groups:
                print(group)

        
    
