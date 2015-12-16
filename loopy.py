#!/usr/bin/env python

import sys
import os
import time

if __name__ == '__main__':

    # write pid to a file to allow service manager to stop this daemon
    pidfile = sys.argv[1]
    with open(os.path.expanduser(pidfile), "w") as f:
        f.write(str(os.getpid()))

    # startup
    print('+ loopy starting')
    sys.stdout.flush()

    # do some work, reporting progress
    for i in range(5):
        print("loop[{}]".format(i))
        sys.stdout.flush()
        time.sleep(5)

    # exit: service manager should restart daemon
    print('- loopy done, exiting')
