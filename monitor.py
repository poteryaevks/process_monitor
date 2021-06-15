import getpass
import psutil


def userName(string):
    strings = string.split('\\')
    return strings[-1]


class Processes:

    def __iter__(self):
        for process in psutil.process_iter(['pid', 'name', 'username']):
            if getpass.getuser() == userName(process.username()):
                yield process
