def deco(func):
    def wrapper():
        startTime = time.time()
        func()
        endTime = time.time()
        msecs = (endTime - startTime)*1000
        print("time is %d ms" %msecs)
    return wrapper

def selfloop(func):
    def start(*args, **kwargs):
        interal = 0
        while(interal < kwargs['loop']):
            print("loop " + interal)
            interal = interal + 1
        return func(*args, **kwargs)
    return start

def deadloop(func):
    pass
