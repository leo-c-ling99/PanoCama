#import tornado
import tornado.ioloop
import tornado.web
import tornado.websocket
import datetime
import asyncio
 
websiteConnections = set()
mcuConnections = set()

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
 
class WebsiteWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        websiteConnections.add(self)
        print("Website WebSocket opened")
 
    def on_message(self, message):
        print(message)
        [client.write_message(message) for client in mcuConnections]
 
    def on_close(self):
        websiteConnections.remove(self)
    
    def check_origin(self, origin):
        return True
        

class EmbeddedWebSocket(tornado.websocket.WebSocketHandler):
    imageByte = bytearray([0xFF])
    left = True

    def open(self):
        mcuConnections.add(self)
        print("MCU WebSocket opened")
 
    def on_message(self, message):
        print(message)
        if message != "Pic Complete":
            self.imageByte += message
        else:
            #start_idx = 0
            end_idx = 0
            # for ii in range(len(self.imageByte)-1):
            #     if 0xFF == self.imageByte[ii] and 0xD8 == self.imageByte[ii+1]:
            #         start_idx = ii
            for ii in range(0, len(self.imageByte)-1):
                if 0xFF == self.imageByte[ii] and 0xD9 == self.imageByte[ii+1]:
                    end_idx = ii + 2

            im_b = bytes(self.imageByte[0:end_idx])
            now = datetime.datetime.now()
            if self.left:
                with open(f"temp/left/test{now.strftime('%H-%M-%S-%f')}.jpg", "wb") as f:
                    f.write(im_b)
                #self.left = False
            else:
                with open(f"temp/right/test{now.strftime('%H-%M-%S-%f')}.jpg", "wb") as f:
                    f.write(im_b)
                #self.left = True
            
            self.imageByte = bytearray([0xFF])
 
    def on_close(self):
        mcuConnections.remove(self)
    
    def check_origin(self, origin):
        return True
 
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", EmbeddedWebSocket),
        (r"/websiteWebsocket", WebsiteWebSocket)
    ])
 
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    app = make_app()
    app.listen(8888)

    tornado.ioloop.IOLoop.current().start()