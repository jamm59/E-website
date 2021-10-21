import smtplib
import os
import math
from time import sleep



def send_mail(message,to_email,from_email):
    host = ''
    if '@gmail' in to_email:
        host = 'smtp.gmail.com'
    else:
        host = 'smtp.mail.yahoo.com'

    with smtplib.SMTP(host) as connection:
        connection.starttls()
        connection.login(email=from_email,password=os.environ.get(''))
        connection.sendmail(from_email,to_email,message)


def count_down(time):
    mins = math.floor(time / 60)
    secs = math.floor(time % 60)
    print(mins, secs)
    if mins == 0 and secs == 0:
        pass
    else:
        sleep(0.05)
        count_down(time-1)

count_down(5*60)