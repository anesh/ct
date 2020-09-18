import ssl
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('echo.websocket.org', 443))
s = ssl.wrap_socket(s, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_SSLv23)
handshake = '\
GET / HTTP/1.1\r\n\
Host: echo.websocket.org\r\n\
Upgrade: websocket\r\n\
Connection: Upgrade\r\n\
Sec-WebSocket-Key: x3JJHMbDL1EzLkh9GBhXDw==\r\n\
WebSocket-Protocol: echo\r\n\
Sec-WebSocket-Version: 13\r\n\r\n\
'
s.send(bytes(handshake))
data = s.recv(1024)
print data

