# import module when need to measure time metrics for scripts
import atexit
from datetime import timedelta
from time import time, strftime, localtime

def seconds_to_str(elapsed=None):
    if elapsed:
        return str(timedelta(seconds=elapsed))
    else:
        return strftime("%Y-%m-%d %H:%M:%S", localtime())

def log(s, elapsed=None):
    line = "=" * 40
    print(line)
    print(f"{seconds_to_str()} - {s}")
    if elapsed:
        print(f"elapsed time: {seconds_to_str(elapsed)}")
    print(line)

def endlog():
    elapsed = time() - start
    log("script ended", elapsed=elapsed)

start = time()
atexit.register(endlog)
log("script started")
