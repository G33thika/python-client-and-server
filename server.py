import socket
import sys
import signal
import threading


try:

    host = sys.argv[1]
    port = int(sys.argv[2])

    #https://blog.miguelgrinberg.com/post/how-to-kill-a-python-thread
    exit_event = threading.Event()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    c_con, c_addr = s.accept()

    def a ():
        while True:
            data = c_con.recv(1024)
            print(data.decode('utf-8'))
            if exit_event.is_set():
                break
        c_con.close()
        sys.exit(1)

    def b ():
        while True:
            msg= input()
            c_con.send(msg.encode('utf-8'))
            if exit_event.is_set():
                break
        c_con.close()
        sys.exit(1)

    def signal_handler(signum, frame):
        exit_event.set()

    signal.signal(signal.SIGINT, signal_handler)

    t1=threading.Thread(target=a)
    t2=threading.Thread(target=b)

    t1.start()
    t2.start()

except OSError:
    print("Address already in use.")
except ValueError:
    print("Enter like this: server.py host port \nport and host check again ")
except IndexError:
    print("Enter like this: server.py [ip_addr] [port]")

    