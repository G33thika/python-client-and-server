import socket
import sys
import signal
import threading

try:
    host = sys.argv[1]
    port = int(sys.argv[2])

    exit_event = threading.Event()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))

    def a ():
        while True:
            msg = input()
            s.send(msg.encode('utf-8'))
            if exit_event.is_set():
                break
        s.close()
        sys.exit(1)

           
    def b ():
        while True:
            res = s.recv(1024)
            print(res.decode('utf-8'))
            if exit_event.is_set():
                break
        s.close()
        sys.exit(1)            

    def signal_handler(signum, frame):
        exit_event.set()


    signal.signal(signal.SIGINT, signal_handler)

    t1=threading.Thread(target=a)
    t2=threading.Thread(target=b)

    t1.start()
    t2.start()

except ValueError:
    print("Enter like this: client.py host port \nport and host check again ")
except IndexError:
    print("Enter like this: client.py [ip_addr] [port]")



    