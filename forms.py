import app,models,utils

class Form():
  ok       = False   # form is valid or not
  fields   = {}      # input data from html form
  warn     = []      # warning messages for every broken rule
  data     = {}      # data returned to the caller {}
  view     = ''      # template name used for the web form
  url      = ''      # redirect url if form was processed
  redirect = False   # if form to be redirected


#---- FORM VALIDATION ----

def messages(request,fid,tid):
  form   = Form()
  fields = request.getForm()

  # sanitize
  author = utils.toStr(fields.get('author','Anonymous'),40)
  uid    = utils.idify(author)
  email  = fields.get('email')
  url    = fields.get('url')
  content= utils.toTxt(fields.get('content',''),9000)

  # validate
  ok=True
  warn=[]
  if email or url or 'http' in content:
    form.ok=False
    form.redirect=True
    form.url='%s/%s/%s'%(app.root,fid,tid)
    return form
  if not author:
    warn.append('You need to identify yourself as the author')
    ok=False
  if author==author.upper():
    warn.append('Author can not be all caps')
    ok=False
  if not content:
    warn.append('You must enter some content')
    ok=False
  if content==content.upper():
    warn.append('Content can not be all caps')
    ok=False

  # process
  if ok:
    form.ok   = True
    form.url  = '%s/%s/%s'%(app.root,fid,tid)
    data      = {'topicid':tid,'forumid':fid,'userid':uid,'author':author,'content':content}
    models.newMessage(data)
  else:
    form.ok   = False
    form.warn = warn
    form.data = {
      'forum'  :models.getForum(fid),
      'topic'  :models.getTopic(tid),
      'list'   :models.getMessages(tid),
      'warn'   :warn,
      'author' :author,
      'content':content
    }
  return form


def newTopic(request,fid):
  form   = Form()
  fields = request.getForm()

  # sanitize
  title  = utils.toStr(fields.get('title',''),80)
  imp    = utils.toInt(fields.get('importance','0'))
  author = utils.toStr(fields.get('author',''),40)
  uid    = utils.idify(author)
  email  = fields.get('email')
  url    = fields.get('url')
  content= utils.toTxt(fields.get('content',''),9000)

  # validate
  ok=True
  warn=[]
  if email or url:
    form.ok=False
    form.redirect=True
    form.url='%s/%s'%(app.root,fid)
    return form
  if not title:
    warn.append('Title can not be empty')
    ok=False
  if title==title.upper():
    warn.append('Title can not be all caps')
    ok=False
  if not author:
    warn.append('You need to identify as the author')
    ok=False
  if author==author.upper():
    warn.append('Author can not be all caps')
    ok=False
  if not content:
    warn.append('You must enter some content')
    ok=False
  if content==content.upper():
    warn.append('Content can not be all caps')
    ok=False
  if ok:
    dat1 = {'forumid':fid,'title':title,'userid':uid,'author':author,'importance':imp}
    rec1 = models.newTopic(dat1)
    tid  = rec1.topicid
    dat2 = {'topicid':tid,'forumid':fid,'userid':uid,'author':author,'content':content}
    rec2 = models.newMessage(dat2)
    form.ok  = True
    form.url = '%s/%s/%s'%(app.root,fid,tid)
  else:
    form.ok   = False
    form.warn = warn
    form.data = {
      'forum'  :models.getForum(fid),
      'warn'   :warn,
      'title'  :title,
      'author' :author,
      'content':content
    }
  return form


def newForum(request):
  form   = Form()
  fields = request.getForm()

  # sanitize
  title = utils.toStr(fields.get('title',''), 80)
  desc  = utils.toStr(fields.get('desc' ,''),120)
  url   = utils.idify(fields.get('url'  ,''), 40)
  order = utils.toInt(fields.get('order'))

  # validate
  ok=True
  warn=[]
  if not url:
    warn.append('Forum needs a permalink')
    ok=False
  if not title:
    warn.append('Title can not be empty')
    ok=False
  if title==title.upper():
    warn.append('Title can not be all caps')
    ok=False
  if not desc:
    warn.append('You must enter some description')
    ok=False
  if desc==desc.upper():
    warn.append('Description can not be all caps')
    ok=False
  if ok:
    if not order: order=models.getNextOrder()
    data = {'url':url,'title':title,'description':desc,'order':order}
    rec  = models.newForum(data)
    form.ok  = True
    form.url = '%s/admin/forum'%(app.root)
  else:
    form.ok   = False
    form.warn = warn
    form.data = {
      'forum'  :models.getForum(fid),
      'warn'   :warn,
      'title'  :title,
      'author' :author,
      'content':content
    }
  return form

#---- END ----