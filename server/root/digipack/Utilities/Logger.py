import time
import sys


def accessLog(message, userId):
    with open("/root/digipack/application/access_logs/" + str(userId) + ".txt", "a+") as log:
        timeC = time.strftime("%d:%m:%Y:%H:%M:%S" ,time.localtime())
        log.write(f'{timeC}: {message}\n')

