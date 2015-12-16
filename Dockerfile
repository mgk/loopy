FROM phusion/baseimage

CMD ["/sbin/my_init"]

RUN ln -s /usr/bin/python3 /usr/bin/python
COPY etc/ /etc/
COPY loopy.py /
