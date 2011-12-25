          # -*- coding: utf-8 -*-
from os import path as op
from pbkdf2 import crypt
import uuid
import datetime
import re
from api import api
from api.models import User
import cgi
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
try:
  from local_settings import *
except ImportError:
  pass


loader = tornado.template.Loader(os.path.join(os.path.dirname(__file__), "templates"))
ROOT = op.normpath(op.dirname(__file__))
# На каком порту зауcкаемся
define("port", default=PORT, type=int)

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

class WebSocketFileHandler(tornado.web.RequestHandler):
    def get(self):
        # Obviously, you want this on CDN, but for sake of
        # example this approach will work.
        self.set_header('Content-Type', 'application/x-shockwave-flash')

        with open(op.join(ROOT, 'static/WebSocketMain.swf'), 'rb') as f:
            self.write(f.read())
            self.finish()

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        user = self.get_secure_cookie("user")
        if not user:
            return None
        return user

    def get_user_id(self):
        user_id = self.get_secure_cookie("user_id")
        return user_id

    def get_user_sex(self):
        username = self.get_current_user()
        user = User.objects.get(username=username)
        print user.is_men

class Registration(BaseHandler):
    men = False
    def get(self):
        self.render("registration.html", error_name=False, error_password=False, error_password_again=False, error_sex=False)

    def post(self):
        error_name = error_password = error_password_again = error_sex = False
        error = False
        try:
            name = self.get_argument("name")
            p = re.compile(u'^[a-zA-Z0-9]*$|^[а-яА-Я0-9]*$')
            m = p.match(name)
            if len(name) > 15:
                error_name = "Логин не должен быть более 15 символов"
                error = True
            elif m:
                for waiter in ChatConnection.waiters:
                    if str(waiter.user_name).lower() == name.encode('utf-8').lower():
                        error_name = "Такой логин уже используется"
                        error = True
                if User.objects.filter(username=name):
                    error_name = "Такой логин уже используется"
                    error = True
            else:
                error_name = "Логин должен состоять из латинских или русских букв"
                error = True
        except :
            error_name = "Укажите логин"
            error = True
        try:
            password = self.get_argument("password")
            if len(password) > 15:
                error_password = "Пароль не должен быть более 15 символов"
                error = True
        except :
            error_password = "Укажите пароль"
            error = True
        try:
            password_again = self.get_argument("password_again")
            if not error_password:
                if not password == password_again:
                    error_password_again = "Пароль не совпадает"
                    error = True
        except :
            error_password_again = "Укажите повторный пароль"
            error = True
        try:
            is_men = self.get_argument("sex")
            if is_men == "True":
                self.men = True
        except :
            error_sex = "Укажите ваш пол"
            error = True
        if error:
            self.render("registration.html", error_name=error_name, error_password=error_password, error_password_again=error_password_again, error_sex=error_sex)
        else:
            new_user = User()
            new_user.username = name
            new_user.password = crypt(password)
            new_user.is_men = self.men
            new_user.save()
            self.set_secure_cookie("user", name)
            self.set_secure_cookie("user_id", str(uuid.uuid4()))
            self.redirect("/")

class AuthLoginHandler(BaseHandler):
  def get(self):
      self.render("login.html", error=False)

  def post(self):
      try:
          name = self.get_argument("name")
          if len(name) > 15:
              self.render("login.html", error="Имя должно состоять Не более чем из 15 символов")
              return
          p = re.compile(u'^[a-zA-Z0-9]*$|^[а-яА-Я0-9]*$')
          m = p.match(name)
          if m:
              print "bbbbb"
              for waiter in ChatConnection.waiters:
                  if str(waiter.user_name) == name.encode('utf-8'):
                      print "11111"
                      self.render("login.html", error="Такое имя уже используется")
                      return
              if User.objects.filter(username=name):
                  print "99999"
                  self.render("login.html", error="Такое имя уже используется")
                  return
              print "oooooo"
              self.set_secure_cookie("user", name)
              self.set_secure_cookie("user_id", str(uuid.uuid4()))
              self.redirect("/")
              return
          else:
              self.render("login.html", error="Имя должно состоять из латинских или русских букв")
              return
      except :
          pass
      try:
          reg_name = self.get_argument("name_reg")
      except :
          self.render("login.html", error="Введите логин")
          return
      try:
          password = self.get_argument("password")
      except :
          self.render("login.html", error="Введите пароль")
          return
      try:
          user = User.objects.get(username=reg_name)
      except :
          self.render("login.html", error="Логин или пароль не верны")
          return
      if user.password == crypt(password, user.password):
          for waiter in ChatConnection.waiters:
              if str(waiter.user_name).lower() == reg_name.encode('utf-8').lower():
                  self.render("login.html", error="Такое имя уже используется")
                  return
          self.set_secure_cookie("user", user.username)
          self.set_secure_cookie("user_id", str(uuid.uuid4()))
          self.redirect("/")
      else:
          self.render("login.html", error="Логин или пароль не верны")
          return


class AuthLogoutHandler(BaseHandler):
  def get(self):
      self.clear_all_cookies()
      self.redirect("/")

class IndexHandler(BaseHandler):
    """Regular HTTP handler to serve the chatroom page"""
    @tornado.web.authenticated
    def get(self):
        self.render('index.html', users_online = map(lambda a: loader.load("user.html").generate(current_user=a[0], id=a[1], sex=a[2]), ChatConnection.users_online), messages = ChatConnection.messages_cache)

class SocketIOHandler(BaseHandler):
    def get(self):
        self.render(op.join(ROOT, '/static/socket.io.js'))

class StatsHandler(BaseHandler):
    def get(self):
        self.render('stats.html')

class ChatConnection(tornadio2.conn.SocketConnection):
    # Class level variable
    waiters = set()
    users_online = []
    messages_cache = []
    cache_size = 40
    user_name = None
    user_id = None
    user_sex = None

    def on_open(self, info):
        self.send(self.users_online)
        self.user_name = self.get_current_user(info)
        self.user_id = self.get_user_id(info)
        self.user_sex = self.get_user_sex(info)
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        new_user = False
        print "Подключился %s" % self.user_name
        if [self.user_name, self.user_id, self.user_sex] not in self.users_online:
            new_user = True
        self.waiters.add(self)
        if new_user:
            message = {
                "type": "new_user",
                "user": loader.load("user.html").generate(current_user=self.user_name, id=self.user_id, sex=self.user_sex),
                "html": loader.load("new_user.html").generate(time = time, current_user=self.user_name, id=self.user_id, sex=self.user_sex),
            }
            self.users_online.append([self.user_name, self.user_id, self.user_sex])
            self.console_message(message)

    def on_message(self, message_src):
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        personals = []
        private = False
        for input in message_src:
            if input['name'] == 'message':
                if not input['value']:
                    return
                else:
                    format_message = api.format_message(cgi.escape(input['value']))
                    message = {
                        "type": "new_message",
                        "html": loader.load("message.html").generate(message=format_message, time = time, current_user=self.user_name, id=self.user_id),
                        "message" : format_message,
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
            ChatConnection.messages_cache.extend([message_for_all])
            if len(ChatConnection.messages_cache) > ChatConnection.cache_size:
                ChatConnection.messages_cache = ChatConnection.messages_cache[1:]
        elif private:
            for waiter in self.waiters:
                if waiter.user_name == private_to:
                    waiter.send(message1)
                if waiter.user_name == self.user_name:
                    waiter.send(message2)
        else:
            for waiter in self.waiters:
                waiter.send(message)
            ChatConnection.messages_cache.extend([message])
            if len(ChatConnection.messages_cache) > self.cache_size:
                ChatConnection.messages_cache = ChatConnection.messages_cache[1:]

    def console_message(self, message):
        for waiter in self.waiters:
            waiter.send(message)
        ChatConnection.messages_cache.extend([message])
        if len(ChatConnection.messages_cache) > self.cache_size:
            ChatConnection.messages_cache = ChatConnection.messages_cache[1:]

    def on_close(self):
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        self.waiters.remove(self)
        if self.user_name not in map(lambda a: a.user_name, self.waiters):
            self.users_online.remove([self.user_name, self.user_id, self.user_sex])
            message = {
                "type": "user_is_out",
                "user_id": self.user_id,
                "html": loader.load("message_out.html").generate(time = time, sex = self.user_sex, current_user = self.user_name, timeout=True),
            }
            self.console_message(message)

    @tornadio2.event('exit')
    def out_user(self, args):
        time = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        self.waiters.remove(self)
        self.users_online.remove([self.user_name, self.user_id, self.user_sex])
        message = {
            "type": "user_is_out",
            "user_id": self.user_id,
            "html": loader.load("message_out.html").generate(time = time, sex = self.user_sex, current_user = self.user_name, timeout=False),
        }
        self.console_message(message)

    def get_current_user(self, info):
        return decode_signed_value(application.settings["cookie_secret"],
                                        "user", info.get_cookie("user").value)
    def get_user_id(self, info):
        return decode_signed_value(application.settings["cookie_secret"],
                                        "user_id", info.get_cookie("user_id").value)
    def get_user_sex(self, info):
        username = decode_signed_value(application.settings["cookie_secret"],
            "user", info.get_cookie("user").value)
        user = User.objects.filter(username=username)
        if user:
            user = User.objects.get(username=username)
            if user.is_men:
                return "male"
            else:
                return "female"
        else:
            return "user"

class PingConnection(tornadio2.conn.SocketConnection):
    @tornadio2.event('ping')
    def ping(self, client):
        now = datetime.datetime.now()
        return client, [now.hour, now.minute, now.second, now.microsecond / 1000]

    @tornadio2.event('stats')
    def stats(self):
        return ChatRouter.stats.dump()

# Create tornadio server
ChatRouter = tornadio2.router.TornadioRouter(ChatConnection,dict(enabled_protocols=['xhr-polling','jsonp-polling','htmlfile'],session_check_interval=15,session_expiry=10))

StatsRouter = tornadio2.router.TornadioRouter(PingConnection, dict(enabled_protocols=['websocket','xhr-polling','jsonp-polling', 'htmlfile'],websocket_check=True),namespace='stats')

urls = ([(r"/", IndexHandler),
         (r"/stats", StatsHandler),
         (r"/socket.io.js", SocketIOHandler),
         (r"/reg", Registration),
         (r"/auth/login", AuthLoginHandler),
         (r"/auth/logout", AuthLogoutHandler),
         (r"/WebSocketMain.swf", WebSocketFileHandler),
        ])

ChatRouter.apply_routes(urls)
StatsRouter.apply_routes(urls)

application = tornado.web.Application(
    urls,
    flash_policy_port = 843,
    flash_policy_file = op.join(ROOT, '/static/flashpolicy.xml'),
    socket_io_port = PORT,
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    xsrf_cookies=True,
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
    debug=True,
    login_url="/auth/login",
)



if __name__ == "__main__":
    tornadio2.server.SocketServer(application)
