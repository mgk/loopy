# Simple Daemon Scripts

Recipe for creating a Linux daemon from a Python, Ruby, or NodeJS script.

Service managers like runit, SysV init, and upstart work great to start daemons but it can be tricky to stop daemons. The [requirements of a well behaved daemon](http://stackoverflow.com/questions/23515165/correct-daemon-behaviour-from-pep-3143-explained) are pretty onerous to add to your script. The [python-daemon](https://pypi.python.org/pypi/python-daemon/) package can handle this for you, but I prefer to keep the daemon logic out of my script as much as possible.

This repo is a demo using runit to run a python script as a daemon that can be cleanly started and stopped and is automatically restarted when it exits. The python script is not burdened with daemon logic.

## `loopy.py`

Example daemon that just prints from time to time. It knows very little about its daemonic nature: it writes its pid to a file, that's it.

## runit setup

[runit](http://smarden.org/runit) is simple and reliable. It restarts your daemon automatically if it exits, which is really useful. This frees your daemon from having complicated try/catch logic that tries to keep it running at all costs while still reporting errors. With runit, just let your daemon exit if it hits a hard error: runit will restart it.

## `/etc/service/loopy/run`

This starts your daemon and sends its standard output to the system logger.

## `/etc/service/loopy/control/t`

This is a runit hook script that is called whenever your service is stopped. Why do we need it? The loopy daemon runs as two processes, and runit only knows about the parent process that it started. The `control/t` script stops the child python process cleanly.

Control hooks are [somewhat buried](http://smarden.org/runit/runsv.8.html#sect4) in the docs, but basically runit lets you run a custom script for each action it takes on a daemon.

## `/etc/service/loopy/control/u`

This hook is run when your service starts. It is a symlink to `t`. It tries to the process and pid file if it is already running. It almost never will be running, so `u` is mostly an extra precaution.

That's it. You can see it in action with docker or use the snippets above in your own daemons.

## Running Demo in Docker

+ `docker build -t loopy --rm .`
+ `docker run -it loopy /sbin/my_init -- bash -l`

You'll see the loopy output every few seconds. After 25 seconds loopy will exit and be restarted automatically. You can do `sv start loopy` and `sv stop loopy`. You can also do `ps -ef` to see that there is one loopy python process when it is started and zero loopy processes when it is stopped.

## References

+ [runit](http://smarden.org/runit)
+ [SO thread](http://stackoverflow.com/questions/473620/how-do-you-create-a-daemon-in-python)
+ [python-daemon](https://pypi.python.org/pypi/python-daemon/) - this works well if you prefer to have your script contain the daemon logic
+ [phusion/baseimage](http://phusion.github.io/baseimage-docker/) - a great way to start the Dockerfile for your image

## License
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
