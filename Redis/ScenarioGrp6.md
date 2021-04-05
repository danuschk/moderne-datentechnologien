# Lecture Modern Data Technologies - Exercise 1 (Redis)

### Group 6

| Name | Matr. Nr. |
|:-----|----------:|
| David Sugar | 76050 |
| xyz | 123 |
| abc | 456 |

### Scenario

We wanna build our own small messaging app using the pubsub paradigm
of [Redis](https://redis.io/) so we can chat with our peers. As
language for the application wee chose to use `Python 3` with the
`redis` package. The idea is to create one channel for every user
where the name of the channel is the username. The channel names are
stored within a `ZSET` (sorted set) where each name is mapped to the
number of subscribed users (each user is subscribed to his/ her own
channel). The username and a status text for each user are stored 
within a `HASH` where the key of each entry is `users:<uname>`. When
a user sends a message, that status text is automatically appended.

... two more data types

### Getting started

First we installed Python by using the `apt` package manager
`sudo apt install python3`. Then we created a new directory `mkdir RChat`
together with a new virtual environment for Python `Python3 -m venv venv`.
After that we sourced the virtual environment `source venv/bin/activate`
and install the `redis` package by executing `pip install redis`.

Then we created a new python file and insert the following code.

```
import redis

if __name__ == '__main__':
    print("Hello, Redis!")
```

Here we import the downloaded `redis` package and print out
a simple message to the command line. The `__name__ == '__main__'`
takes care that the following code is just executed if the file
is executed as main script.

### Implementation
