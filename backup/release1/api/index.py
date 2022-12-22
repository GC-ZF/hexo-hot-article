"""
@Author:张时贰
@Date:2022年12月20日
@CSDN:张时贰
@Blog:zhangshier.vip
"""
import json
import time
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
from api.Post_Table_Release2 import run


class handler ( BaseHTTPRequestHandler ):
    def do_GET(self):
        try:
            path = self.path.split ( '?' )[ 1 ]
            path = 'https://' + path
            print ( path )
            data = run ( path )
            self.send_response ( 200 )
            self.send_header ( 'Access-Control-Allow-Origin', '*' )
            self.send_header ( 'Cache-Control', 'no-cache' )
            self.send_header ( 'Content-type', 'application/json' )
            self.end_headers ()
            self.wfile.write ( json.dumps ( data ).encode ( 'utf-8' ) )
            return
        except Exception as e:
            e = str ( e )
            data = [ {'msg': e} ]
            self.send_response ( 404 )
            self.send_header ( 'Access-Control-Allow-Origin', '*' )
            self.send_header ( 'Cache-Control', 'no-cache' )
            self.send_header ( 'Content-type', 'application/json' )
            self.end_headers ()
            self.wfile.write ( json.dumps ( data ).encode ( 'utf-8' ) )


if __name__ == '__main__':
    print ( 1 )
    # server = HTTPServer ( ('localhost', 8080), handler )
    # server.serve_forever ()
