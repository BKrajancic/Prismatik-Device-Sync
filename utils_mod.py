
from operator import truediv
from utils import _screengrab_average
import time

def _main():
    while True:
        t1 = time.time()
        out = _screengrab_average()
        t2 = time.time()
        print ("- Time2 %2.4f" % (t2-t1))
        time.sleep(1)

if __name__ == "__main__":
    _main()