
# coding: utf-8

# In[ ]:


import http.server
from http.server import HTTPServer,SimpleHTTPRequestHandler
import ssl
import base64

cust_response = """
<html>
<head>
<title>Mantappu</title>
</head>

<body>
<h1 style="text-align:center"><b><i>Hello World!</i></b><h1>
</body>
</html>
"""

userName = "admin"
passWord = "admins"
auth_keyWord = userName +":"+ passWord
auth_keyWord_b64 = "Basic " + str(base64.b64encode(auth_keyWord.encode("utf-8")),"utf-8")


class RequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_HEAD(self):
        print ("send header")
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_AUTHHEAD(self):
        print ("send header")
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Test\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #global auth_key
        ''' Present frontpage with user authentication. '''
        if self.headers.get('authorization') == None:
            self.do_AUTHHEAD()
            self.wfile.write(b'no auth header received')
            pass
        elif self.headers.get('authorization') == auth_keyWord_b64:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.send_header("Content-length",len(cust_response))
            self.end_headers()
            self.wfile.write(str.encode(cust_response))
        else:
            self.do_AUTHHEAD()
            self.wfile.write(b'not authenticated')
            pass


port = 8594
with HTTPServer(("",port), RequestHandler) as httpd:
    print("serving at port ",port)
    httpd.socket = ssl.wrap_socket(httpd.socket, keyfile = "key.pem", certfile = "cert.pem", server_side=True)
    httpd.serve_forever()

