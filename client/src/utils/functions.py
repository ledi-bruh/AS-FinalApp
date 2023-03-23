from datetime import datetime


def now():
    time = datetime.now()
    return time.strftime('%d:%m:%Y %H:%M:%S')


def at_time(func):
    def wrapper(*args, **kwargs):
        if type(f := func(*args, **kwargs)) is str:
            return f'{now()}: {f}'
        else:
            return f
    return wrapper
