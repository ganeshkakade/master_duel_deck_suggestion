# import module when need to measure time metrics for scripts
import atexit
from time import time, strftime, localtime
from datetime import timedelta

def seconds_to_str(elapsed=None):
    if elapsed:
        return str(timedelta(seconds=elapsed))
    else:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

def log(s, elapsed=None):
    line = "=" * 40
    print(line)
    print(seconds_to_str(), '-', s)
    if elapsed:
        print("elapsed time:", elapsed)
    print(line)

def endlog():
    end = time()
    elapsed = end - start
    log("script ended", seconds_to_str(elapsed))

start = time()
atexit.register(endlog)
log("script started")
