import tornado.ioloop
import tornado.web
from lzstring import LZString
from pathlib import Path
import json
import glob
import os
import errno
import base64



class MainHandler(tornado.web.RequestHandler):
    

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
  

    def post(self):
        # self.write("Hello, world")
        
        # print("%r %s" % (self.request, self.request.body.decode()))
        args = json.loads(self.request.body.decode())
        # print j['hat']

        cmd = args['cmd']

        if cmd == "poke": 
            filePath = args["filePath"]
            out = {};
            out["exists"] = str(os.path.exists(filePath));
            out["isDir"] = str(os.path.isdir(filePath))

            self.write(json.dumps(out))

        #list directory
        elif cmd == "ls": 
            out = []
            requestedData = args["plzSend"];

            filePath = args["filePath"]
            files = glob.glob(filePath+"*")
            for file in files:
                addMe = {
                    'name' : file,
                    'isDir' : str(os.path.isdir(file))
                }

                if "size" in requestedData:
                    addMe["size"] = os.path.getsize(file)

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

            # dataType = ""
            # if dataType in args:
            dataType = args["dataType"]

            print(dataType);


            if dataType == "png":
                fullData = LZString.decompress(data)
                print(fullData)
                imgdata = base64.decodestring(fullData.encode())
                # imgdata = base64.b64decode(data)
                # imgdata = base64.b64decode())

                with open(filePath, "wb") as file:
                    file.write(imgdata)

            else:
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
    # x = lzstring.LZString()
    # data64 = x.decompress("▃偂༠䨎ڐ")
    # print(data64)
    

    # my_ioloop = tornado.ioloop.IOLoop.current()
    # my_ioloop.close(all_fds=True)
    app = make_app()
    app.listen(8528)
    tornado.ioloop.IOLoop.current().start()

