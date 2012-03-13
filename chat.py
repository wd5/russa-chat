          # -*- coding: utf-8 -*-
from os import path as op
import json
from django.core.exceptions import ValidationError
from pbkdf2 import crypt
import uuid
import datetime
import re
import time
from api import api
from api.models import User, Quote, Anekdote
from api.mixins import VKMixin
import cgi
import tornado
from tornado.options import define
import tornado.web
import tornado.httpserver
import os.path
from tornado.web import decode_signed_value
import tornado.ioloop
import tornado.web

import sockjs.tornado

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

class BaseHandler(tornado.web.RequestHandler, VKMixin):
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
        user = User.objects.filter(username=username)
        try:
            access_token = self.get_secure_cookie('access_token')
        except :
            access_token = False
        if user:
            user = User.objects.get(username=username)
            if user.is_men:
                return "male"
            else:
                return "female"
        elif access_token:
            return self.get_secure_cookie('sex')
        else:
            return "user"
    
    def is_vk(self):
        if self.get_secure_cookie("access_token"):
            return True
        else:
            return False

class Registration(BaseHandler):
    men = False
    def get(self):
        self.render("registration.html", error_name=False, error_password=False, error_password_again=False, error_sex=False)

    def post(self):
        errors = []
        try:
            name = self.get_argument("name")
            p = re.compile(u'^[a-zA-Z0-9_]*$|^[а-яА-Я0-9_]*$')
            m = p.match(name)
            if len(name) > 15:
                error = {
                    "input_name": "name",
                    "error": u'Логин не должен быть более 15 символов'
                }
                errors.append(error)
            elif m:
                for waiter in ChatConnection.waiters:
                    if str(waiter.user_name).lower() == name.encode('utf-8').lower():
                        error = {
                            "input_name": "name",
                            "error": u'Такой логин уже используется'
                        }
                        errors.append(error)
                if User.objects.filter(username=name):
                    error = {
                        "input_name": "name",
                        "error": u'Такой логин уже используется'
                    }
                    errors.append(error)
            else:
                error = {
                    "input_name": "name",
                    "error": u'Логин должен состоять из латинских или русских букв'
                }
                errors.append(error)
        except :
            error = {
                "input_name": "name",
                "error": u'Укажите логин'
            }
            errors.append(error)
        try:
            password = self.get_argument("password")
            if len(password) > 15:
                error = {
                    "input_name": "password",
                    "error": u'Пароль не должен быть более 15 символов"'
                }
                errors.append(error)
        except :
            error = {
                "input_name": "password",
                "error": u'Укажите пароль'
            }
            errors.append(error)
        try:
            password_again = self.get_argument("password_again")
            if not password == password_again:
                error = {
                    "input_name": "password_again",
                    "error": u'Пароль не совпадает'
                }
                errors.append(error)
        except :
            error = {
                "input_name": "password_again",
                "error": u'Укажите повторный пароль'
            }
            errors.append(error)
        try:
            is_men = self.get_argument("sex")
            if is_men == "True":
                self.men = True
        except :
            error = {
                "input_name": "sex",
                "error": u'Укажите ваш пол'
            }
            errors.append(error)
        if errors:
            self.write(json.dumps(errors))
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
      self.render("login.html", error=False, input_error=False)

  def post(self):
      try:
          name = self.get_argument("name")
          if len(name) > 15:
              self.render("login.html", error="Имя должно состоять Не более чем из 15 символов", input_error="name")
              return
          p = re.compile(u'^[a-zA-Z0-9_]*$|^[а-яА-Я0-9_]*$')
          m = p.match(name)
          if m:
              for waiter in ChatConnection.waiters:
                  if str(waiter.user_name) == name.encode('utf-8'):
                      self.render("login.html", error="Такое имя уже используется", input_error="name")
                      return
              if User.objects.filter(username=name):
                  self.render("login.html", error="Такое имя уже используется", input_error="name")
                  return
              self.set_secure_cookie("user", name)
              self.set_secure_cookie("user_id", str(uuid.uuid4()))
              self.redirect("/")
              return
          else:
              self.render("login.html", error="Имя должно состоять из латинских или русских букв", input_error="name")
              return
      except :
          try:
              self.get_argument("is_guestform")
              self.render("login.html", error="Введите гостевой логин", input_error="name")
          except:
	      pass
      try:
          reg_name = self.get_argument("name_reg")
      except :
          self.render("login.html", error="Введите логин", input_error="name_reg")
          return
      try:
          password = self.get_argument("password")
      except :
          self.render("login.html", error="Введите пароль", input_error="password")
          return
      try:
          user = User.objects.get(username=reg_name)
      except :
          self.render("login.html", error="Логин или пароль не верны", input_error="name_reg")
          return
      if user.password == crypt(password, user.password):
          for waiter in ChatConnection.waiters:
              if str(waiter.user_name).lower() == reg_name.encode('utf-8').lower():
                  self.render("login.html", error="Такое имя уже используется", input_error="name_reg")
                  return
          self.set_secure_cookie("user", user.username)
          self.set_secure_cookie("user_id", str(uuid.uuid4()))
          self.redirect("/")
      else:
          self.render("login.html", error="Логин или пароль не верны", input_error="name_reg")
          return


class AuthLogoutHandler(BaseHandler):
  def get(self):
      self.clear_all_cookies()
      self.redirect("/")
      time_now = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
      username = self.get_current_user()
      userid = self.get_user_id()
      sex = self.get_user_sex()
      message = {
          "type": "user_is_out",
          "user_id": userid,
          "html": loader.load("message_out.html").generate(time = time_now, sex = sex, current_user = username, timeout=False),
          }
      for waiter in ChatConnection.waiters:
          waiter.send(message)
          if waiter.user_name == username:
              waiter_del = waiter
      try:
          ChatConnection.waiters.remove(waiter_del)
      except :
          pass
      ChatConnection.messages_cache.extend([message])
      if len(ChatConnection.messages_cache) > ChatConnection.cache_size:
          ChatConnection.messages_cache = ChatConnection.messages_cache[1:]
      count = 0
      for user in ChatConnection.users_online:
          count +=1
          if user[0] == username:
              del ChatConnection.users_online[count-1]

class IndexHandler(BaseHandler):
    """Regular HTTP handler to serve the chatroom page"""
    @tornado.web.authenticated
    def get(self):
        for i in ChatConnection.users_online:
            if i[0] == self.get_current_user():
                if not i[1] == self.get_user_id():
                    self.render("login.html", error="Кто то уже сидит под этим ником", input_error="name_reg")
                    return
        try:
            profile = User.objects.get(username=self.get_current_user())
            self.render('index.html',sex=self.get_user_sex(), is_vk = self.is_vk(), users_online = map(lambda a: loader.load("user.html").generate(current_user=a[0], id=a[1], sex=a[2], away=a[3], profile=a[4]), ChatConnection.users_online), quantity=len(ChatConnection.users_online), messages = ChatConnection.messages_cache, profile=profile)
        except :
            profile = False
            self.render('index.html',sex=self.get_user_sex(), is_vk = self.is_vk(), users_online = map(lambda a: loader.load("user.html").generate(current_user=a[0], id=a[1], sex=a[2], away=a[3], profile=a[4]), ChatConnection.users_online), quantity=len(ChatConnection.users_online), messages = ChatConnection.messages_cache, profile=profile)

class ProfileHandler(BaseHandler):
    """Regular HTTP handler to serve the chatroom page"""
    @tornado.web.authenticated
    def get(self, profile_id):
        try:
            profile = User.objects.get(id=profile_id)
            self.render('profile.html', profile=profile)
        except :
            pass

class PostProfile(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        errors = []
        p = re.compile(u'^[a-zA-Z]*$|^[а-яА-Я]*$')
        name = self.get_argument("name","").title()
        if name:
            m = p.match(name)
            if len(name) > 15:
                error = {
                    "input_name": "name",
                    "error": u'Имя не должно превышать 15 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "name",
                    "error": u'Имя должно состоять из латинских или русских букв'
                    }
                errors.append(error)
        surname = self.get_argument("surname","").title()
        if surname:
            m = p.match(surname)
            if len(surname) > 15:
                error = {
                    "input_name": "surname",
                    "error": u'Фамилия не должна превышать 15 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "surname",
                    "error": u'Фамилия должна состоять из латинских или русских букв'
                    }
                errors.append(error)
        patronymic = self.get_argument("patronymic","").title()
        if patronymic:
            m = p.match(patronymic)
            if len(patronymic) > 15:
                error = {
                    "input_name": "patronymic",
                    "error": u'Отчество не должно превышать 15 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "patronymic",
                    "error": u'Отчество должно состоять из латинских или русских букв'
                    }
                errors.append(error)
        day = self.get_argument("day","")
        month = self.get_argument("month","")
        year = self.get_argument("year","")
        if year:
            if int(year) < 1940:
                error = {
                    "input_name": "year",
                    "error": u'А вы не слишком стары для этого?'
                    }
                errors.append(error)
            elif int(year) > 2010:
                error = {
                    "input_name": "year",
                    "error": u'В детский сад не опаздаешь?'
                    }
                errors.append(error)
        birthplace = self.get_argument("birthplace","")
        if birthplace:
            if len(birthplace) > 30:
                error = {
                    "input_name": "birthplace",
                    "error": u'Родной город не должен превышать 30 символов'
                    }
                errors.append(error)
        liveplace = self.get_argument("liveplace","")
        if liveplace:
            if len(liveplace) > 30:
                error = {
                    "input_name": "liveplace",
                    "error": u'Город проживания не должен превышать 30 символов'
                    }
                errors.append(error)
        phone = self.get_argument("phone","")
        if phone:
            p = re.compile(u'^[0-9-\ ()]*$')
            m = p.match(phone)
            if len(phone) > 15:
                error = {
                    "input_name": "phone",
                    "error": u'Телефон не должен превышать 15 симфолов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "phone",
                    "error": u'Недопустимые символы в телефоне'
                    }
                errors.append(error)
        skype = self.get_argument("skype","").lower()
        if skype:
            p = re.compile(u'^[0-9a-zA-Z]*$')
            m = p.match(skype)
            if len(skype) > 32:
                error = {
                    "input_name": "skype",
                    "error": u'Skype не должен превышать 32 символа'
                    }
                errors.append(error)
            elif len(skype) < 6:
                error = {
                    "input_name": "skype",
                    "error": u'Skype не должен быть меньше 6 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "skype",
                    "error": u'Имя Skype должно быть латинскими буквами'
                    }
                errors.append(error)
        vkontakte = self.get_argument("vkontakte","")
        if vkontakte:
            p = re.compile(u'^http:\/\/(www\.)?vk\.com|vkontakte\.ru\/[a-zA-z0-9\.\_\-]*$')
            m = p.match(vkontakte)
            if len(vkontakte) > 50:
                error = {
                    "input_name": "vkontakte",
                    "error": u'Адрес vkontakte не должен быть более 50 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "vkontakte",
                    "error": u'Не верный адрес vkontakte'
                    }
                errors.append(error)
        facebook = self.get_argument("facebook","")
        if facebook:
            p = re.compile(u'^http:\/\/(www\.)?facebook\.com\/[a-zA-z0-9\.\_\-]*$')
            m = p.match(facebook)
            if len(facebook) > 50:
                error = {
                    "input_name": "facebook",
                    "error": u'Адрес facebook не должен быть более 50 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "facebook",
                    "error": u'Не верный адрес facebook'
                    }
                errors.append(error)
        twitter = self.get_argument("twitter","")
        if twitter:
            p = re.compile(u'^https?:\/\/(www\.)?twitter\.com\/[a-zA-z0-9\.\_\-\#\!\/]*$')
            m = p.match(twitter)
            if len(twitter) > 50:
                error = {
                    "input_name": "twitter",
                    "error": u'Адрес twitter не должен быть более 50 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "twitter",
                    "error": u'Не верный адрес twitter'
                    }
                errors.append(error)
        site = self.get_argument("site","")
        if site:
            p = re.compile(u'^https?:\/\/(?P<name>[a-zA-Z0-9-_\.\/?=%\&\+\;]+)')
            m = p.match(site)
            if len(site) > 100:
                error = {
                    "input_name": "site",
                    "error": u'Адрес сайта не должен быть более 100 символов'
                    }
                errors.append(error)
            elif not m:
                error = {
                    "input_name": "site",
                    "error": u'Не верный адрес сайта'
                    }
                errors.append(error)
        work = self.get_argument("work","")
        if work:
            if len(work) > 15:
                error = {
                    "input_name": "work",
                    "error": u'Место работы не должно быть более 15 символов'
                    }
                errors.append(error)
        school = self.get_argument("school","")
        if school:
            if len(school) > 15:
                error = {
                    "input_name": "school",
                    "error": u'Школа не должна быть более 15 символов'
                    }
                errors.append(error)
        institute = self.get_argument("institute","")
        if institute:
            if len(institute) > 15:
                error = {
                    "input_name": "institute",
                    "error": u'Институт не должен быть более 15 символов'
                    }
                errors.append(error)
                pass
        about = self.get_argument("about","")
        if about:
            if len(about) > 300:
                error = {
                    "input_name": "about",
                    "error": u'О себе не более 300 символов.'
                    }
                errors.append(error)
        profile = User.objects.get(username=self.get_current_user())
        if errors:
            self.write(json.dumps(errors))
        else:
            if name:
                profile.name=name
            if surname:
                profile.surname=surname
            if day:
                if month:
                    if year:
                        profile.birthday = str(year + "-" + month + "-" + day)
            if patronymic:
                profile.patronymic=patronymic
            if birthplace:
                profile.birthplace=birthplace
            if liveplace:
                profile.liveplace=liveplace
            if phone:
                profile.phone=phone
            if skype:
                profile.skype=skype
            if vkontakte:
                profile.vkontakte=vkontakte
            if facebook:
                profile.facebook=facebook
            if twitter:
                profile.twitter=twitter
            if site:
                profile.site=site
            if work:
                profile.work=work
            if school:
                profile.school=school
            if institute:
                profile.institute=institute
            if about:
                profile.about=about
            try:
                profile.save()
            except ValidationError, e:
                if e.messages == [u'Invalid date: day is out of range for month']:
                    error = {
                        "input_name": "month",
                        "error": u'В этом месяце нет такого дня'
                    }
                    errors.append(error)
                elif e.messages == [u'Invalid date: month must be in 1..12']:
                    error = {
                        "input_name": "month",
                        "error": u'Нет такого месяца'
                    }
                    errors.append(error)
                elif e.messages == [u'Enter a valid date in YYYY-MM-DD format.']:
                    error = {
                        "input_name": "month",
                        "error": u'Неправильный формат даты'
                    }
                    errors.append(error)
                self.write(json.dumps(errors))

class SocketIOHandler(BaseHandler):
    def get(self):
        self.render(op.join(ROOT, '/static/socket.io.js'))

class StatsHandler(BaseHandler):
    def get(self):
        self.render('stats.html')

class ChatConnection(sockjs.tornado.SockJSConnection):
    # Class level variable
    waiters = set()
    users_online = []
    messages_cache = []
    cache_size = 40
    user_name = None
    user_id = None
    user_sex = None
    away = False
    profile = None
    first_message_time = None
    count_message = 0

    def on_open(self, info):
        self.user_name = self.get_current_user(info)
        self.waiters.add(self)
        self.user_id = self.get_user_id(info)
        for i in self.users_online:
            if i[0] == self.user_name:
                if not i[3] == False:
                    i[3] = False
                    drop_away = {
                        "type": "drop_away",
                        "user_id": self.user_id
                    }
                    for waiter in self.waiters:
                        waiter.send(drop_away)
        self.send(self.users_online)
        self.user_sex = self.get_user_sex(info)
        if not self.user_sex == "user":
            self.profile = self.get_profile_link(info)
        time_now = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        new_user = False
        print "Подключился %s" % self.user_name
        if [self.user_name, self.user_id, self.user_sex, self.away, self.profile] not in self.users_online:
            new_user = True
        if new_user:
            message = {
                "type": "new_user",
                "user": loader.load("user.html").generate(current_user=self.user_name, id=self.user_id, sex=self.user_sex, away=self.away, profile=self.profile),
                "html": loader.load("new_user.html").generate(time = time_now, current_user=self.user_name, id=self.user_id, sex=self.user_sex),
            }
            self.users_online.append([self.user_name, self.user_id, self.user_sex, self.away, self.profile])
            self.console_message(message)
            if len(ChatConnection.users_online) < 5:
                message = {
                    "type": "new_message",
                    "html": loader.load("system_message.html").generate(time = time_now, message="В данный момент в чате мало народу, не уходите а просто оставьте вкладку открытой, только так здесь будет с кем поговорить:)"),
                    }
                self.send(message)

    def on_message(self, message_src):
        for i in self.waiters:
            print i.user_name
        message_src = json.loads(message_src)
        self.count_message+=1
        if self.first_message_time:
            self.last_message_time = time.time()
            if int(str(self.last_message_time - self.first_message_time).split(".")[0]) > 3:
                self.first_message_time = None
                self.count_message = 0
            elif self.count_message > 5:
                message = {
                    "type": "kick",
                    }
                for waiter in self.waiters:
                    if waiter.user_name == self.user_name:
                        waiter_del = waiter
                        waiter.send(message)
                try:
                    ChatConnection.waiters.remove(waiter_del)
                except :
                    pass
        else:
            self.first_message_time = time.time()
        time_now = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        personals = []
        private = False
        for input in message_src:
            if input['name'] == 'message':
                if not input['value']:
                    return
                else:
                    if len(input['value']) > 500:
                        return
                    format_message = api.format_message(cgi.escape(input['value']))
                    if format_message[:5] == '/away':
                        i = self.users_online.index([self.user_name, self.user_id, self.user_sex, self.away, self.profile])
                        self.away = True
                        message = {
                            "type": "status",
                            "user_id": self.user_id,
                            "status" : self.away,
                            }
                        for waiter in self.waiters:
                            waiter.send(message)
                        self.users_online[i] = [self.user_name, self.user_id, self.user_sex, self.away, self.profile]
                        return
                    elif format_message[:6] == '/kick ':
                        if self.user_name == 'Владимир':
                            kick_name = format_message[6:]
                            message = {
                                "type": "kick",
                                }
                            for waiter in self.waiters:
                                if waiter.user_name == kick_name.encode('utf-8'):
                                    waiter_del = waiter
                                    waiter.send(message)
                            try:
                                ChatConnection.waiters.remove(waiter_del)
                            except :
                                pass
                            return
                    elif format_message[:7] == u'/цитата':
                        citata = Quote.objects.order_by('?')[0]
                        message = {
                            "type": "new_message",
                            "html": loader.load("console_message.html").generate(time = time_now, current_user=self.user_name, id=self.user_id, sex=self.user_sex, msg=citata, type=True),
                            "message" : format_message,
                            }
                        self.send(message)
                        if self.away:
                            drop_away = {
                                "type": "drop_away",
                                "user_id": self.user_id
                            }
                            i = self.users_online.index([self.user_name, self.user_id, self.user_sex, self.away, self.profile])
                            self.away = False
                            self.users_online[i] = [self.user_name, self.user_id, self.user_sex, self.away, self.profile]
                            for waiter in self.waiters:
                                waiter.send(drop_away)
                        return
                    elif format_message[:8] == u'/анекдот':
                        anekdote = Anekdote.objects.order_by('?')[0]
                        message = {
                            "type": "new_message",
                            "html": loader.load("console_message.html").generate(time = time_now, current_user=self.user_name, id=self.user_id, sex=self.user_sex, msg=anekdote, type=False),
                            "message" : format_message,
                            }
                        self.send(message)
                        if self.away:
                            drop_away = {
                                "type": "drop_away",
                                "user_id": self.user_id
                            }
                            i = self.users_online.index([self.user_name, self.user_id, self.user_sex, self.away, self.profile])
                            self.away = False
                            self.users_online[i] = [self.user_name, self.user_id, self.user_sex, self.away, self.profile]
                            for waiter in self.waiters:
                                waiter.send(drop_away)
                        return
                    else:
                        message = {
                            "type": "new_message",
                            "html": loader.load("message.html").generate(message=format_message, time = time_now, current_user=self.user_name, id=self.user_id),
                            "message" : format_message,
                        }
                        if self.away:
                            drop_away = {
                                "type": "drop_away",
                                "user_id": self.user_id
                            }
                            i = self.users_online.index([self.user_name, self.user_id, self.user_sex, self.away, self.profile])
                            self.away = False
                            self.users_online[i] = [self.user_name, self.user_id, self.user_sex, self.away, self.profile]
                            for waiter in self.waiters:
                                waiter.send(drop_away)
            elif input['name'] == 'personal[]':
                if input['value']:
                    personals.append(input['value'])
            elif input['name'] == 'private':
                if input['value']:
                    for waiter in self.waiters:
                        if waiter.user_id == input['value']:
                            private_to = waiter
                    print u'\033[1;41mПриват от %s для %s: %s\033[1;m' % (self.user_name.decode('utf-8'), private_to.user_name, message["message"])
                    message1 = {
                        "private" : "True",
                        "type": "new_message",
                        "html": loader.load("private_message_outgoing.html").generate(message=message["message"], time = time_now, current_user=self.user_name, id=self.user_id, who="тебя"),
                    }
                    message2 = {
                        "private" : "True",
                        "type": "new_message",
                        "html": loader.load("private_message_incoming.html").generate(message=message["message"], time = time_now, current_user=self.user_name, id=self.user_id, who=private_to),
                    }
                    private = True
        if personals:
            personals_name = set()
            message_for_all = {}
            outgoing_message = {}
            for waiter in self.waiters:
                if waiter.user_id in personals:
                    personals_name.add(waiter)
            message["html"] = loader.load("personal_message_incoming.html").generate(message=message["message"], time = time_now, current_user=self.user_name, id=self.user_id, personals=personals_name)
            message["personal"] = "True"
            outgoing_message["html"] = loader.load("personal_message_outgoing.html").generate(message=message["message"], time = time_now, current_user=self.user_name, id=self.user_id, personals=personals_name)
            outgoing_message["type"] = "new_message"
            message_for_all["html"] = loader.load("personal_message_all.html").generate(message=message["message"], time = time_now, current_user=self.user_name, id=self.user_id, personals=personals_name)
            message_for_all["type"] = "new_message"
            del message["message"]
            for waiter in self.waiters:
                if waiter.user_id in personals:
                    waiter.send(message)
                elif waiter.user_id == self.user_id:
                    waiter.send(outgoing_message)
                else:
                    waiter.send(message_for_all)
            ChatConnection.messages_cache.extend([message_for_all])
            if len(ChatConnection.messages_cache) > ChatConnection.cache_size:
                ChatConnection.messages_cache = ChatConnection.messages_cache[1:]
        elif private:
            for waiter in self.waiters:
                if waiter.user_name == private_to.user_name:
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
        try:
            self.waiters.remove(self)
            tornado.ioloop.IOLoop.instance().add_timeout(time.time() + 6, self.check_user)
        except :
            return

    def check_user(self):
        time_now = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
        if self.user_name not in map(lambda a: a.user_name, self.waiters):
            self.users_online.remove([self.user_name, self.user_id, self.user_sex, self.away, self.profile])
            message = {
                    "type": "user_is_out",
                    "user_id": self.user_id,
                    "html": loader.load("message_out.html").generate(time = time_now, sex = self.user_sex, current_user = self.user_name, timeout=True),
                }
            self.console_message(message)

    def get_current_user(self, info):
        return decode_signed_value(app.settings["cookie_secret"],
                                        "user", info.get_cookie("user").value)
    def get_user_id(self, info):
        return decode_signed_value(app.settings["cookie_secret"],
                                        "user_id", info.get_cookie("user_id").value)
    def get_user_sex(self, info):
        username = decode_signed_value(app.settings["cookie_secret"],
            "user", info.get_cookie("user").value)
        try:
            sex = decode_signed_value(app.settings["cookie_secret"],
                "sex", info.get_cookie("sex").value)
            return sex
        except :
            pass
        user = User.objects.filter(username=username)
        if user:
            user = User.objects.get(username=username)
            if user.is_men:
                return "male"
            else:
                return "female"
        else:
            return "user"

    def get_profile_link(self, info):
        try:
            access_token = decode_signed_value(app.settings["cookie_secret"],
                "access_token", info.get_cookie("access_token").value)
            id = decode_signed_value(app.settings["cookie_secret"],
                "user_id", info.get_cookie("user_id").value)
            return "http://vk.com/id%s" % id
        except :
            user = User.objects.get(username=self.user_name)
            return "/profile/%s" % user.id


class PingConnection(sockjs.tornado.SockJSConnection):
#    @tornadio2.event('ping')
    def ping(self, client):
        now = datetime.datetime.now()
        return client, [now.hour, now.minute, now.second, now.microsecond / 1000]

#    @tornadio2.event('stats')
    def stats(self):
        return ChatRouter.stats.dump()

class VKHandler(BaseHandler, VKMixin):
  @tornado.web.asynchronous
  def get(self):
      self.clear_all_cookies()
      time_now = datetime.datetime.time(datetime.datetime.now()).strftime("%H:%M")
      username = self.get_current_user()
      userid = self.get_user_id()
      sex = self.get_user_sex()
      if username:
          message = {
              "type": "user_is_out",
              "user_id": userid,
              "html": loader.load("message_out.html").generate(time = time_now, sex = sex, current_user = username, timeout=False),
              }
          for waiter in ChatConnection.waiters:
              waiter.send(message)
              if waiter.user_name == username:
                  waiter_del = waiter
          try:
              ChatConnection.waiters.remove(waiter_del)
          except :
              pass
          ChatConnection.messages_cache.extend([message])
          if len(ChatConnection.messages_cache) > ChatConnection.cache_size:
              ChatConnection.messages_cache = ChatConnection.messages_cache[1:]
          count = 0
          for user in ChatConnection.users_online:
              count +=1
              if user[0] == username:
                  del ChatConnection.users_online[count-1]

      if self.get_argument("code", None):
          self.get_authenticated_user(self.async_callback(self._on_auth))
          return

      args = {
          "response_type": "code",
          "scope": "friends"
      }

      self.authorize_redirect(client_id=self.settings["client_id"], redirect_uri="http://russa-chat.ru/vkauth", extra_params=args)

  def _on_auth(self, user):
      if not user:
          raise tornado.web.HTTPError(500, "Auth failed")
      name = tornado.escape.xhtml_escape(user["response"][0]["first_name"])
      if len(name) > 15:
          name = name[:15]
      p = re.compile(u'^[a-zA-Z0-9_]*$|^[а-яА-Я0-9_]*$')
      m = p.match(name)
      not_unique = True
      if m:
          name = name.encode('utf-8')
          raw_name = name
          while not_unique:
              i = 0
              for waiter in ChatConnection.waiters:
                  if str(waiter.user_name) == name:
                      i += 1
                      name = raw_name + str(i)
                      continue
              if User.objects.filter(username=name):
                  i += 1
                  name = raw_name + str(i)
              not_unique = False
          self.set_secure_cookie("user", name)
          self.set_secure_cookie("user_id", str(user['response'][0]['uid']))
          self.set_secure_cookie("access_token", user['access_token'])
          self.vk_request(self.async_callback(self._set_sex), access_token=user['access_token'], api_method="getProfiles", params={"uids": user['response'][0]['uid'], "fields": "sex"})
      else:
          self.render("login.html", error="Имя должно состоять из латинских или русских букв")

  def _set_sex(self, response):
      sex = response['response'][0]['sex']
      if sex == 2:
          sex = "male"
      else:
          sex = "female"
      self.set_secure_cookie("sex", sex)
      self.redirect("/")

class VKTest(BaseHandler, VKMixin):
    @tornado.web.authenticated
    @tornado.web.asynchronous
    def get(self):
        access_token = self.get_secure_cookie("access_token")
        self.vk_request(self.async_callback(self._on_test), access_token=access_token, api_method="getProfiles", params={"uids": self.get_user_id(), "fields": "sex"})

    def _on_test(self, response):
        # "response" is json-response from server
        self.redirect("/")


if __name__ == "__main__":
    import logging
    logging.getLogger().setLevel(logging.DEBUG)

    # 1. Create chat router
    ChatRouter = sockjs.tornado.SockJSRouter(ChatConnection,user_settings=dict(disabled_transports=['websocket','xhr_streaming']))

    # 2. Create Tornado application
    app = tornado.web.Application(
        [(r"/", IndexHandler),
            (r"/stats", StatsHandler),
            (r"/socket.io.js", SocketIOHandler),
            (r"/reg", Registration),
            (r"/profile/([0-9]+)", ProfileHandler),
            (r"/profile", PostProfile),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/vkauth", VKHandler),
            (r"/test", VKTest),
        ] + ChatRouter.urls,
        cookie_secret="43oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        debug=DEBUG,
        login_url="/auth/login",
        xsrf_cookies=True,
        client_id=2644170,
        client_secret="2Z8zrQH5wFGJGLGHOt3u",
    )

    # 3. Make Tornado app listen on port 8080
    app.listen(PORT)

    # 4. Start IOLoop
    tornado.ioloop.IOLoop.instance().start()
