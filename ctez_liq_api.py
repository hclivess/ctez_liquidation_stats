import tornado.ioloop
import tornado.web
import ctez_liq_collector

import threading
import time

import ctez_liq_tweet


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write(ctez_liq_collector.read_database())

class ReadHandler(tornado.web.RequestHandler):
    def get(self):
        liquidations = ctez_liq_collector.read_database()

        self.render("liquidations.html",
                    title="ctez Oven Liquidations",
                    liquidations=liquidations)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/read", ReadHandler),
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": "static"}),
    ])


class ThreadedClient(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                ctez_liq_collector.run()
                ctez_liq_tweet.pick()

                run_interval = 360
                print(f"Sleeping for {run_interval / 60} minutes")
                time.sleep(run_interval)
            except Exception as e:
                print(f"Error: {e}")


if __name__ == "__main__":
    background = ThreadedClient()
    #background.start()
    print("Background process started")

    app = make_app()
    app.listen(1236)
    print("Main process starting")
    tornado.ioloop.IOLoop.current().start()
