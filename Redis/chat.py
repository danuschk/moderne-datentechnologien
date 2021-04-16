import redis
import sys

# https://docs.python.org/3.5/howto/curses.html

class Chat:
    GROUPS = 'GROUPS'
    USERS = 'users'
    ACTIVE_USERS = 'active'
    MESSAGES = 'messages'

    def __init__(self, ip, port):
        self.r = redis.Redis(host=ip, port=port, db=0)
        print(self.r)

    def set(self, key, val):
        return self.r.set(key, val)

    def get(self, key):
        return self.r.get(key)

    def get_users(self):
        """
        Get all available groups to join.
        """
        return self.r.smembers(self.ACTIVE_USERS)

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
        # Hash user info        :: (HASH)
        self.chat.r.hset("{}:{}".format(chat.USERS, uname), 'uname', uname)
        self.chat.r.hset("{}:{}".format(chat.USERS, uname), 'status', status)

        # Zset of sent messages per user(group) :: (ZSET)
        self.chat.r.zadd(chat.GROUPS, { uname : 0.0 })

        # Add user to active users :: (SET)
        self.chat.r.sadd(chat.ACTIVE_USERS, uname)

        # Enter pub/ sub and subscribe to own channel
        self.channel = chat.r.pubsub()
        self.channel.subscribe(uname)

    def __del__(self):
        self.chat.r.srem(chat.ACTIVE_USERS, self.uname)

    def get_message(self):
        msg = self.channel.get_message()
        if msg:
            message = msg['data']

            if message != None and message != 1:
                msg = message.decode('utf-8')
                self.chat.r.lpush("{}:{}".format(chat.MESSAGES, self.uname), msg)
                self.chat.r.zincrby(chat.GROUPS, -1.0, self.uname)
                return msg
            else:
                return ""

    def send_message(self, dst, msg):
        # Increment the sent message count
        self.chat.r.zincrby(chat.GROUPS, 1.0, dst)
        return self.chat.r.publish(dst, "From {}: {}\n--------------------\n{}\n--------------------\n".format(self.uname, self.status, msg))

    def received_messages(self):
        return self.chat.r.zscore(chat.GROUPS, self.uname)

    def get_history(self):
        return self.chat.r.lrange("{}:{}".format(chat.MESSAGES, self.uname), 0, -1)


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
        elif t[0] == 'getusers':
            groups = user.chat.get_users()
            for group in groups:
                print(group.decode('utf-8'))
        elif t[0] == 'received':
            print("{} messages".format(user.received_messages()))
        elif t[0] == 'history':
            for msg in user.get_history():
                print(msg.decode('utf-8'))
        else:
            print("send name message - Send a message to a user with the given name\nget - get all new messages\ngetusers - show all active users\nreceived - show how many new messages have been received\nhistory - show all messages received")

        
    
