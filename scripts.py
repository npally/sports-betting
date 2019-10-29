import time
from datetime import date


def get_week():
    week = 0
    today = date.today()

    if today < date(2019, 9, 11):
        week = 1
        return week

    elif today < date(2019, 9, 17):
        week = 2
        return week

    elif today < date(2019, 9, 24):
        week = 3
        return week

    elif today <= date(2019, 10, 1):
        week = 4
        return week

    elif today <= date(2019, 10, 8):
        week = 5
        return week

    elif today <= date(2019, 10, 15):
        week = 6
        return week

    elif today <= date(2019, 10, 22):
        week = 7
        return week

    elif today <= date(2019, 10, 29):
        week = 8
        return week

    elif today <= date(2019, 11, 5):
        week = 9
        return week

    elif today <= date(2019, 11, 12):
        week = 10
        return week

    elif today <= date(2019, 11, 19):
        week = 11
        return week

    elif today <= date(2019, 11, 26):
        week = 12
        return week

    elif today <= date(2019, 12, 3):
        week = 13
        return week

    elif today <= date(2019, 12, 10):
        week = 14
        return week

    elif today <= date(2019, 12, 17):
        week = 15
        return week

    elif today <= date(2019, 12, 24):
        week = 16
        return week

    elif today <= date(2020, 12, 31):
        week = 17
        return week

    
