import redis
import sys

# https://docs.python.org/3.5/howto/curses.html

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
        # Hash user info
        self.chat.r.hset("{}:{}".format(chat.USERS, uname), 'uname', uname)
        self.chat.r.hset("{}:{}".format(chat.USERS, uname), 'status', status)
        # Zset of sent messages per user(group)
        self.chat.r.zadd(chat.GROUPS, { uname : 0.0 })

        # Enter pub/ sub and subscribe to own channel
        self.channel = chat.r.pubsub()
        self.channel.subscribe(uname)

    def get_message(self):
        msg = self.channel.get_message()
        if msg:
            message = msg['data']

            if message != None and message != 1:
                self.chat.r.zincrby(chat.GROUPS, -1.0, self.uname)
                return message.decode('utf-8')
            else:
                return ""

    def send_message(self, dst, msg):
        # Increment the sent message count
        self.chat.r.zincrby(chat.GROUPS, 1.0, dst)
        return self.chat.r.publish(dst, "From {}: {}\n--------------------\n{}\n--------------------\n".format(self.uname, self.status, msg))

    def received_messages(self):
        return self.chat.r.zscore(chat.GROUPS, self.uname)


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
                if message == None:
                    break;
                else:
                    print(message)
        elif t[0] == 'getgroups':
            groups = user.chat.get_groups()
            for group in groups:
                print(group)
        elif t[0] == 'received':
            print("{} messages".format(user.received_messages()))
        else:
            print("send name message\nget\ngetgroups")

        
    
