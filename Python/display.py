def sendStatus(status):
    try:
        conn = httplib.HTTPConnection("192.168.1.121", 9080)
        conn.request("GET", "/?display=" + urllib.quote(status))
        response = conn.getresponse()
        print response.status, response.reason
    except Exception as e:
        print("[Errno {0}] {1}".format(e, e))