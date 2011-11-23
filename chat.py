          # -*- coding: utf-8 -*-
from os import path as op
import uuid
import datetime
import tornado
from tornado.options import define
import tornado.web
import tornado.httpserver
import tornadio2
import tornadio2.router
import tornadio2.server
import tornadio2.conn
import os.path
import logging
from tornado.web import decode_signed_value


loader = tornado.template.Loader(os.path.join(os.path.dirname(__file__), "templates"))
ROOT = op.normpath(op.dirname(__file__))
# На каком порту запсукаемся
define("port", default=8005, type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", IndexHandler),
            (r"/socket.io.js", SocketIOHandler),
        ]
        settings = dict(
            static_path=os.path.join(os.path.dirname(__file__), "static"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return user

    def get_user_id(self):
        user_id = self.get_secure_cookie("user_id")
        return user_id

class AuthLoginHandler(BaseHandler):
  def get(self):
      self.render("login.html")

  def post(self):
      name = self.get_argument("name")
      self.set_secure_cookie("user", name)
      self.set_secure_cookie("user_id", str(uuid.uuid4()))
      self.redirect("/")

class AuthLogoutHandler(BaseHandler):
  def get(self):
      self.clear_all_cookies()
      self.redirect("/")

class IndexHandler(BaseHandler):
    """Regular HTTP handler to serve the chatroom page"""
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', users_online = ChatConnection.users_online, messages = ChatConnection.messages_cache)

class SocketIOHandler(BaseHandler):
    def get(self):
        self.render('/Users/vladimir/PycharmProjects/my-chat2/static/socket.io.js')

class ChatConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    waiters = set()
    users_online = []
    messages_cache = []
    cache_size = 20
    user_name = None
    user_id = None

    def on_open(self, info):
        self.user_name = self.get_current_user(info)
        self.user_id = self.get_user_id(info)
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        new_user = False
        print "Подключился %s" % self.user_name
        if loader.load("user.html").generate(current_user=self.user_name, id=self.user_id) not in self.users_online:
            new_user = True
        self.waiters.add(self)
        if new_user:
            message = {
                "type": "new_user",
                "user": loader.load("user.html").generate(current_user=self.user_name, id=self.user_id),
                "html": loader.load("new_user.html").generate(time = time, current_user=self.user_name, id=self.user_id),
            }
            self.users_online.append(message["user"])
            self.console_message(message)

    def on_message(self, message_src):
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        personals = []
        private = False
        for input in message_src:
            print input['name']
            if input['name'] == 'message':
                message = {
                    "type": "new_message",
                    "html": loader.load("message.html").generate(message=input['value'], time = time, current_user=self.user_name, id=self.user_id),
                    "message" : input['value'],
                }
            elif input['name'] == 'personal[]':
                if input['value']:
                    personals.append(input['value'])
            elif input['name'] == 'private':
                if input['value']:
                    for waiter in self.waiters:
                        if waiter.user_id == input['value']:
                            private_to = waiter.user_name
                    message1 = {
                        "private" : "True",
                        "type": "new_message",
                        "html": loader.load("private_message.html").generate(message=message["message"], time = time, current_user=self.user_name, id=self.user_id, who="тебя"),
                    }
                    message2 = {
                        "private" : "True",
                        "type": "new_message",
                        "html": loader.load("private_message.html").generate(message=message["message"], time = time, current_user=self.user_name, id=self.user_id, who=private_to),
                    }
                    private = True
        if personals:
            personals_name = set()
            message_for_all = {}
            for waiter in self.waiters:
                if waiter.user_id in personals:
                    personals_name.add(waiter.user_name)
            message["html"] = loader.load("personal_message.html").generate(message=message["message"], time = time, current_user=self.user_name, id=self.user_id, personals=personals_name)
            message["personal"] = "True"
            message_for_all["html"] = loader.load("personal_message_all.html").generate(message=message["message"], time = time, current_user=self.user_name, id=self.user_id, personals=personals_name)
            message_for_all["type"] = "new_message"
            del message["message"]
            for waiter in self.waiters:
                if waiter.user_id in personals:
                    waiter.send(message)
                else:
                    waiter.send(message_for_all)
            self.messages_cache.extend([message_for_all])
            if len(self.messages_cache) > self.cache_size:
                self.messages_cache = self.messages_cache[-self.cache_size:]
        elif private:
            for waiter in self.waiters:
                if waiter.user_name == private_to:
                    waiter.send(message1)
                else:
                    waiter.send(message2)
        else:
            for waiter in self.waiters:
                waiter.send(message)
            self.messages_cache.extend([message])
            if len(self.messages_cache) > self.cache_size:
                self.messages_cache = self.messages_cache[-self.cache_size:]

    def console_message(self, message_src):
        for waiter in self.waiters:
            waiter.send(message_src)

    def on_close(self):
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        self.waiters.remove(self)
        if self.user_name not in map(lambda a: a.user_name, self.waiters):
            self.users_online.remove(loader.load("user.html").generate(current_user=self.user_name, id=self.user_id))
            message = {
                "type": "user_is_out",
                "user_id": self.user_id,
                "html": loader.load("message_out.html").generate(message="%s ушел(timeout)" % self.user_name, time = time),
            }
            self.console_message(message)

    @tornadio2.event('exit')
    def out_user(self, args):
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        self.waiters.remove(self)
        self.users_online.remove(loader.load("user.html").generate(current_user=self.user_name, id=self.user_id))
        message = {
            "type": "user_is_out",
            "user_id": self.user_id,
            "html": loader.load("message_out.html").generate(message="%s ушел(timeout)" % self.user_name, time = time),
        }
        self.console_message(message)

    def get_current_user(self, info):
        return decode_signed_value(application.settings["cookie_secret"],
                                        "user", info.get_cookie("user").value)
    def get_user_id(self, info):
        return decode_signed_value(application.settings["cookie_secret"],
                                        "user_id", info.get_cookie("user_id").value)

# Create tornadio server
ChatRouter = tornadio2.router.TornadioRouter(ChatConnection)

# Create socket application
application = tornado.web.Application(
    ChatRouter.apply_routes([(r"/", IndexHandler),
        (r"/socket.io.js", SocketIOHandler),
        (r"/auth/login", AuthLoginHandler),
        (r"/auth/logout", AuthLogoutHandler)]),
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
    socket_io_port = 8005,
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=True,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    debug=True,
    login_url="/auth/login",
)

if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)
    tornadio2.server.SocketServer(application)
