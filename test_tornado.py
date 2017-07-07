import tornado.ioloop
import tornado.web
from pathlib import Path
import json
import glob
import os
import errno



class MainHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
  

    def post(self):
        # self.write("Hello, world")
        
        # print("%r %s" % (self.request, self.request.body.decode()))
        args = json.loads(self.request.body.decode())
        # print j['hat']

        cmd = args['cmd']

        #list directory
        if cmd == "ls": 
            out = []
            filePath = args["filePath"]
            files = glob.glob(filePath+"*")
            for file in files:
                addMe = {
                    'name' : file,
                    'size' : os.path.getsize(file),
                    'isDir' : str(os.path.isdir(file))
                }
                out.append(addMe)
            
            self.write(json.dumps(out))
          

        #make directory
        elif cmd == "mkdir":
            filePath = args["filePath"]
            name = args["name"]
            try:
                os.makedirs(filepath+name)
                self.write("created")
            except OSError as exception:
                if exception.errno == errno.EEXIST:
                    self.write("exists")
                else:
                    raise
            
        #save file        
        elif cmd == "put":
            filePath = args["filePath"]
            Path(filePath).touch()

            writeType = args["writeType"]
            data = args["data"]
            with open(filePath, writeType) as file:
                file.write(data)

        #get file        
        elif cmd == "get":
            filePath = args["filePath"]
            try:
                with open(filePath) as file:
                    self.write(file.read())

            except IOError:
                raise

        else:
            self.write("Hello, world")

       


    get = post


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8528)
    tornado.ioloop.IOLoop.current().start()

