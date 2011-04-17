import os,sys,traceback,models,utils
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext import db
template.register_template_library('forum.filters')

root = '/forum'

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
  

# use 'run' if you only use one route to one controller
def run(url,main):
  run_wsgi_app(webapp.WSGIApplication([(url,main)],debug=config.debug))

# use 'control' if you use many routers and controllers
# pass 'controller' as list of tuples like [(route1,control1),(route2,control2),...]
def control(controller):
  run_wsgi_app(webapp.WSGIApplication(controller,debug=config.debug))


