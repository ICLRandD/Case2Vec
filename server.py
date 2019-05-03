import os
import json
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.web import url
from gensim.models.word2vec import Word2Vec
import gensim
import re
import pyfiglet


class IndexHandler(tornado.web.RequestHandler):
    """Main handler."""

    def get(self, *args, **kwargs):
        self.render("index.html")


class W2vhookHandler(tornado.web.RequestHandler):
    """RESTful API handler."""

    # def set_default_headers(self):
    # print("setting headers!!!")
    # self.set_header("Access-Control-Allow-Origin", "*")
    # self.set_header("Access-Control-Allow-Headers", "x-requested-with")
    # self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def get(self, *args, **kwargs):
        self.render("index.html")

    def post(self, *args, **kwargs):
        try:
            data = json.loads(self.request.body.decode("utf-8"))
        except:
            print("slack webhook access.")
        try:
            username = self.get_argument("user_name")
        except:
            username = data["user_name"]
        try:
            text = (
                self.get_argument("text").replace("w2v:", "").strip().replace(" ", "")
            )
        except:
            text = data["text"].replace("w2v:", "").strip().replace(" ", "")
        pos, neg = self._proc(text)
        try:
            result = wordvec.most_similar(positive=pos, negative=neg)
        except KeyError as err:
            result = str(err)
        if username == "webapp":
            response = {"text": result}
        else:
            response = {"text": str(result)}
        self.write(json.dumps(response))

    @staticmethod
    def _proc(var):
        div = re.split("([＋－+-])", var)
        sign = 0
        pos = list()
        neg = list()
        for i in range(len(div)):
            if div[i] == "+" or div[i] == "＋":
                sign = 0
            elif div[i] == "-" or div[i] == "－":
                sign = 1
            else:
                pos.append(div[i]) if sign == 0 else neg.append(div[i])
        return (pos, neg)


class Application(tornado.web.Application):
    """Application configuration"""

    def __init__(self, debug):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        tornado.web.Application.__init__(
            self,
            [
                url(r"/", IndexHandler, name="index"),
                url(r"/w2vhook", W2vhookHandler, name="w2vhook"),
            ],
            template_path=os.path.join(BASE_DIR, "templates"),
            static_path=os.path.join(BASE_DIR, "static"),
            debug=debug,
        )


if __name__ == "__main__":
    ascii_banner = pyfiglet.figlet_format("Case2Vec")
    print("Semantic Word2Vec experimentation with case law data by ICLR&D")
    print(ascii_banner)
    with open("config.json") as json_data:
        config = json.load(json_data)
    print("Loading Case2Vec vector model...")
    if config["fasttext"]:
        wordvec = gensim.models.KeyedVectors.load_word2vec_format(
            config["model"], binary=False
        )
    else:
        model = Word2Vec.load(config["model"])
        wordvec = model.wv
    print("Case2Vec model load complete.")
    print("Listening on localhost:8000")
    app = Application(config["debug"])
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
