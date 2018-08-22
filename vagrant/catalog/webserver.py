from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import cgi
from database_setup import Restaurant

engine = create_engine('sqlite:///restaurantmenu.db')
Session = sessionmaker(bind=engine)

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Hello!</h1>"
                output += ("<form method='POST' enctype='multipart/form-data' action='/hello'>"
                           "<h2>What would you like me to say?</h2>"
                           "<input name='message' type='text'>"
                           "<input type='submit' value='Submit'></form>")
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>&#161Hola!</h1>"
                output += ("<form method='POST' enctype='multipart/form-data' action='/hello'>"
                           "<h2>What would you like me to say?</h2>"
                           "<input name='message' type='text'>"
                           "<input type='submit' value='Submit'></form>")
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body><h1>Restaurants</h1>"

                with session_scope() as session:
                    restaurants = session.query(Restaurant).all()
                    for restaurant in restaurants:
                        output += "<h2> %s " % restaurant.name
                        output += "<a href='#'>edit</a> "
                        output += "<a href='#'>delete</a>"
                        output += "</h2>"
                        
                output += "</html></body>"
                self.wfile.write(output)
                print output
                return



        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

            output = ""
            output += "<html><body>"
            output += "<h2>Okay, how about this: </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]

            output += ("<form method='POST' enctype='multipart/form-data' action='/hello'>"
                       "<h2>What would you like me to say?</h2>"
                       "<input name='message' type='text'>"
                       "<input type='submit' value='Submit'></form>")
            output += "</body></html>"
            self.wfile.write(output)
            print output

        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()

if __name__ == '__main__':
    main()
