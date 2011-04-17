import utils
from google.appengine.ext import db
from google.appengine.api import images

#---- FORUM ----------------------------------------------

class ForumUsers(db.Model):
  created     = db.DateTimeProperty(auto_now_add=True)
  userid      = db.StringProperty()
  username    = db.StringProperty()
  nickname    = db.StringProperty()
  password    = db.StringProperty()
  email       = db.StringProperty()
  ipaddress   = db.StringProperty()
  lastlogin   = db.DateTimeProperty()
  isadmin     = db.IntegerProperty(default=0)   # 0.no      1.yes
  inactive    = db.IntegerProperty(default=0)   # 0.active  1.inactive  2.banned

class ForumList(db.Model):
  created     = db.DateTimeProperty(auto_now_add=True)
  updated     = db.DateTimeProperty()
  forumid     = db.StringProperty()
  order       = db.IntegerProperty()
  title       = db.StringProperty()
  description = db.StringProperty(multiline=True)
  ntopics     = db.IntegerProperty(default=0)
  nmessages   = db.IntegerProperty(default=0)
  lastuser    = db.StringProperty()

class ForumTopics(db.Model):
  created     = db.DateTimeProperty(auto_now_add=True)
  updated     = db.DateTimeProperty(auto_now_add=True)
  forumid     = db.StringProperty()
  topicid     = db.StringProperty()
  title       = db.StringProperty()
  userid      = db.StringProperty()
  author      = db.StringProperty()
  nmessages   = db.IntegerProperty()
  nviews      = db.IntegerProperty()
  lastuser    = db.StringProperty()
  importance  = db.IntegerProperty()  #0.normal  1.important 2.pinned
  status      = db.IntegerProperty()  #0.pending 1.approved  2.spam

class ForumMessages(db.Model):
  created     = db.DateTimeProperty(auto_now_add=True)
  updated     = db.DateTimeProperty(auto_now_add=True)
  forumid     = db.StringProperty()
  topicid     = db.StringProperty()
  messageid   = db.StringProperty()
  userid      = db.StringProperty()
  author      = db.StringProperty()
  content     = db.TextProperty()
  status      = db.IntegerProperty()  #0.pending  1.approved  2.spam


class ForumImages(db.Model):
  imageid    = db.StringProperty()   # key_name
  created    = db.DateTimeProperty(auto_now_add=True)
  title      = db.StringProperty()
  format     = db.StringProperty()   # jpg, gif, png
  size       = db.IntegerProperty()
  width      = db.IntegerProperty()
  height     = db.IntegerProperty()
  bits       = db.BlobProperty(default=None)



#---- FORUM ----
def getForums(n=10):
  recs = ForumList.all().order('order').fetch(n)
  return recs

def getForum(fid):
  if not fid: return None
  rec = ForumList.get_by_key_name(fid)
  return rec

def newForum(data):
  key = data['url']
  rec = ForumList(key_name=key)
  #ec.created     = 
  #ec.updated     = 
  rec.forumid     = key
  rec.order       = data['order']
  rec.title       = data['title']
  rec.description = data['description']
  rec.ntopics     = 0
  rec.nmessages   = 0
  #ec.lastuser    = data['']
  rec.put()
  return rec

def getNextOrder(n=100):
  recs = ForumList.all().order('order').fetch(n)
  last = recs[-1]
  return last.order+1

def deleteForum(fid):
  if not fid: return None
  forum    = ForumList.get_by_key_name(fid)
  topics   = ForumTopics.all().filter('forumid =',fid).fetch(999)
  messages = ForumMessages.all().filter('forumid =',fid).fetch(999)
  db.delete(messages)
  db.delete(topics)
  db.delete(forum)
  return fid


#---- TOPICS ----
def getTopics(fid,n=30):
  if not fid: return None
  recs = ForumTopics.all().filter('forumid =',fid).order('-status').order('-updated').fetch(n)
  return recs

def getTopic(tid):
  if not tid: return None
  rec = ForumTopics.get_by_key_name(tid)
  return rec

def viewTopic(tid):
  if not tid: return None
  rec = ForumTopics.get_by_key_name(tid)
  if not rec: return None
  rec.nviews+=1
  rec.put()
  return rec

def newTopic(data):
  key = utils.newKey()
  rec = ForumTopics(key_name=key)
  rec.topicid     = key
  rec.forumid     = data['forumid']
  rec.title       = data['title']
  rec.userid      = data['userid']
  rec.author      = data['author']
  rec.nmessages   = 0
  rec.nviews      = 0
  rec.lastuser    = data['author']
  rec.importance  = data['importance']
  rec.status      = 0
  rec.put()
  topicCounter(rec.forumid)
  return rec


#---- MESSAGES ----
def getMessages(tid,n=30):
  if not tid: return None
  recs = ForumMessages.all().filter('topicid =',tid).order('created').fetch(n)
  return recs

def getMessage(mid):
  if not mid: return None
  rec = ForumMessages.get_by_key_name(mid)
  return rec

def newMessage(data):
  key = utils.newSerial()
  rec = ForumMessages(key_name=key)
  rec.messageid   = key
  rec.topicid     = data['topicid']
  rec.forumid     = data['forumid']
  rec.userid      = data['userid']
  rec.author      = data['author']
  rec.content     = db.Text(data['content'])
  rec.status      = 0
  rec.put()
  messageCounter(rec.topicid,rec.author)
  return rec

def viewMessages(fid,tid):
  if not fid or not tid: return None
  data={
    'forum':getForum(fid),
    'topic':viewTopic(tid),
    'list' :getMessages(tid)
  }
  return data


#---- USERS ----
def getUsers(n=30):
  recs = ForumUsers.all().order('nickname').fetch(n)
  return recs

def getUser(uid):
  if not uid: return None
  rec = ForumUsers.get_by_key_name(uid)
  return rec

def newUser(data):
  key = data['nickname']
  rec = ForumUsers(key_name=key)
  rec.userid     = data['userid']
  rec.username   = data['username']
  rec.nickname   = data['nickname']
  #ec.password   = data['password']
  rec.email      = data['email']
  rec.ipaddress  = data['ipaddress']
  #ec.lastlogin  = data['lastlogin']
  rec.isadmin    = data['isadmin']
  rec.put()
  return rec


#---- IMAGES ----
def getImagesList(page=1,n=50):
  data  = ForumImages.all().order('-created').fetch(n)
  return data

def saveImage(bits,name=None):
  if not bits: return None
  if not name: name=utils.randomString()
  image = ForumImages(key_name=name)
  format,width,height=utils.getImageInfo(bits)
  image.imageid = name
  image.format  = format
  image.width   = width
  image.height  = height
  image.size    = len(bits)
  image.bits    = db.Blob(bits)
  image.put()
  return name

def removeImage(imageid):
  if not imageid: return None
  img = ForumImages.get_by_key_name(imageid)
  if img: img.delete()
  return


#---- UTILS ----
def messageCounter(tid,lastuser):
  topic = getTopic(tid)
  if topic:
    now=utils.now()
    topic.nmessages+=1
    topic.updated   =now
    topic.lastuser  =lastuser
    topic.put()
    forum = getForum(topic.forumid)
    if forum:
      forum.nmessages+=1
      forum.updated   =now
      forum.lastuser  =lastuser
      forum.put()

def topicCounter(fid):
  forum = getForum(fid)
  if forum:
    forum.ntopics+=1
    forum.put()


#---- ADMIN ----
def latestTopics(n=10):
  recs = ForumTopics.all().order('-created').fetch(n)
  return recs

def latestMessages(n=10):
  recs = ForumMessages.all().order('-created').fetch(n)
  return recs

def latestUsers(n=10):
  recs = ForumUsers.all().order('-created').fetch(n)
  return recs

#---- END OF PROGRAM ----------------------------------------------
