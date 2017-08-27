import functools

from adodbapi import Date


def log(func):
    @functools.wraps(func)
    def wrapper(*args,**kw):
        print('begin call %s() method' % func.__name__)
        func(*args,**kw)
        print('end call %s() method' % func.__name__)
    return wrapper

@log
def now():
    print('2017-8-26')
#now()

def logger(text):
    if isinstance(text,str):
        def decorator(func):
            @functools.wraps(func)
            def wrapper(*args,**kw):
                print('now call %s() method,the params within decorator is %s' % (func.__name__ ,text))
                func(*args,**kw)
            return wrapper
        return decorator
    else:
        func = text
        @functools.wraps(func)
        def wrapper(*args,**kw):
            print('now call %s() methodwithout params' % func.__name__ )
            func(*args,**kw)
        return wrapper

@logger('test params')
def print_now():
    print('2017-8-26')
@logger
def print_number():
    print(9527)

print_now()
print_number()
