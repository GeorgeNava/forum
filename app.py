import os,sys,traceback,models,utils
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
template.register_template_library('forum.filters')

root = '/forum'

class routes():
  index    = root
  messages = root+'/(.*)/(.*)'
  newtopic = root+'/newtopic/(.*)'
  topics   = root+'/(.*)'

class config():
  server   = os.environ['SERVER_NAME']
  isLive   = server=='www.example.com'
  isBeta   = server=='example.appspot.com'
  isLocal  = server=='localhost'
  debug    = not isLive
  viewdir  = ''
  viewext  = 'html'
  admin    = 'Forum <georgenava@gmail.com>'
  contact  = 'Forum <georgenava@gmail.com>'


# We extended 'webapp.RequestHandler' to reduce code cluttering
class request(webapp.RequestHandler):
  server    = os.environ['SERVER_NAME']     if 'SERVER_NAME'     in os.environ.keys() else ''
  referer   = os.environ['HTTP_REFERER']    if 'HTTP_REFERER'    in os.environ.keys() else ''
  ipaddress = os.environ['REMOTE_ADDR']     if 'REMOTE_ADDR'     in os.environ.keys() else ''
  useragent = os.environ['HTTP_USER_AGENT'] if 'HTTP_USER_AGENT' in os.environ.keys() else ''
  session  = {}

  def setPlain(self):
    # call before any output
    self.response.headers["Content-Type"] = "text/plain"

  def out(self,text):
    self.response.out.write(text)

  def write(self,text):
    self.response.out.write(text+'\n')

  def show(self,view,data={}):
    if not '.' in view: view=view+'.'+config.viewext                      # no extension? use .html
    if '/' in view: path=os.path.join(os.path.dirname(__file__),view)    # absolute path? use it!
    else: path=os.path.join(os.path.dirname(__file__),config.viewdir,view)  # no path? use default!
    data['root']   =root
    data['session']=self.session
    self.response.out.write(template.render(path,data))

  def getForm(self):
    # TODO: multiple values for same key
    data = dict((key,self.request.get(key,'')) for key in self.request.arguments())
    return data

  def getFile(self,input):
    return self.request.get(input,None)

  def getFileName(self,input):
    name=''
    file=self.request.POST.get(input)
    if file!='': name=os.path.basename(file.filename)
    return name
  
  def startSession(self):
    self.session = Session(self)

  def endSession(self):
    self.session.invalidate()
    self.session = {}

  def logout(self):
    self.session.clearCookies()


# use 'run' if you only use one route to one controller
def run(url,main):
  run_wsgi_app(webapp.WSGIApplication([(url,main)],debug=config.debug))

# use 'control' if you use many routers and controllers
# pass 'controller' as list of tuples like [(route1,control1),(route2,control2),...]
def control(controller):
  run_wsgi_app(webapp.WSGIApplication(controller,debug=config.debug))


#---- SESSION --------------------------------------------------
import random
from google.appengine.api import memcache

class Session(dict):
  def __init__(self,handler):
    self.handler  = handler
    self.ipaddress= handler.request.remote_addr
    self._timeout = 1800 # 30 min
    self._name    = 'sid'
    self._new     = True
    self._invalid = False
    dict.__init__(self)
    name=self._name
    
    ok=False
    if name in handler.request.str_cookies:
      self._sid=handler.request.str_cookies[name]
      data=memcache.get(self._sid)
      if data!=None:
        self.update(data)
        memcache.set(self._sid,data,self._timeout)
        self._new=False
    else: 
      self._sid = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in xrange(12))
      handler.response.headers.add_header('Set-Cookie','%s=%s; path=/;'%(self._name,self._sid))
      ok=True

    if 'uid' in handler.request.str_cookies:
      userid=handler.request.str_cookies['uid']
      self['userid'] = userid
      if 'tid' in handler.request.str_cookies:
        token = handler.request.str_cookies['tid']
        user  = models.userAutologin(userid,token)
        if user:
          self['username']  = user.username
          self['islogged']  = True
          self['lastlogin'] = utils.now()
          self['lastip']    = handler.ipaddress
        else:
          self['islogged']  = False
      ok=True
    if ok: self.save()

  def clearCookies(self):
    headers = self.handler.response.headers
    headers.add_header('Set-Cookie','sid=; path=/; expires=Sat, 1-Jan-2000 00:00:00 GMT;')
    headers.add_header('Set-Cookie','tid=; path=/; expires=Sat, 1-Jan-2000 00:00:00 GMT;')
    headers.add_header('Set-Cookie','uid=; path=/; expires=Sat, 1-Jan-2000 00:00:00 GMT;')
    headers.add_header('Set-Cookie','usr=; path=/; expires=Sat, 1-Jan-2000 00:00:00 GMT;')
    headers.add_header('Set-Cookie','device=; path=/; expires=Sat, 1-Jan-2000 00:00:00 GMT;')

  def save(self):
    if not self._invalid:
      memcache.set(self._sid,self.copy(),self._timeout)

  def isNew(self):
    return self._new  #if session was created during this request

  def isValid(self):
    if 'uid' in self and not self['uid']=='': return True
    else: return False

  def Id(self):
    return self._sid

  def invalidate(self):
    """Delete session data and cookie."""
    self.handler.response.headers.add_header('Set-Cookie','sid=; expires=Sat, 1-Jan-2000 00:00:00 GMT;')
    memcache.delete(self._sid)
    self.clear()
    self._invalid=True

"""
session={
  'userid'    :'',
  'username'  :'',
  'token'     :'',
  'islogged'  :'',
  'lastlogin' :'',
  'lastip'    :'',
  'device'    :'desktop|mobile'
}
"""