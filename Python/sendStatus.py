import httplib, urllib, base64, json
from multiprocessing import Process
import time

def sendStatus(ip, status, delay):
    Process(target=httpSend, args=(ip,status,delay,)).start()

def httpSend(ip,status, delay):
    try:
        time.sleep(delay)
        print status
        conn = httplib.HTTPConnection(ip, 9080)
        conn.request("GET", "/?display=" + urllib.quote(status))
        response = conn.getresponse()
        print response.status, response.reason
    except Exception as e:
        print("[Errno {0}] {1}".format(e, e))

if __name__ == '__main__':
    sendStatus('no makeup', 1)
    sendStatus('beard', 2)
    sendStatus('a natural beauty', 0)
