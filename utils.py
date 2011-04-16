# -*- coding: latin-1 -*-

import app
import os,datetime,time,string,re,random,StringIO,struct,hashlib
from google.appengine.ext import db
from google.appengine.api import mail


#---- DATA CONVERSION ----
def toUid(s,min=0,max=None):
  s = re.sub(r'[^a-zA-Z0-9]','',s)
  if len(s)<min: return ''
  if max: s=s[:max]
  return s

def toStr(s,max=None):
  if not s or s=='' or s=='None': return ''
  if max: s=s[:max]
  s = s.strip().replace('\r\n',' ').replace('\n',' ').replace('\r',' ')
  return s
    
def toTxt(s,max=None):
  if not s or s=='' or s=='None': return ''
  s = re.sub(' +',' ',s)
  if max: s=s[:max]
  return s

def toPsw(s,min=0,max=None):
  # chars and numbers only
  if not s or s=='' or s=='None': return ''
  if len(s)<min: return ''
  if max: s=s[:max]
  s=re.sub(r'[^a-zA-Z0-9]','',s)
  return s

def toDat(s):
  # yyyy-mm-dd
  if not s or s=='' or s=='None': return None
  try:    
    date=(int(s[0:4]),int(s[5:7]),int(s[8:10]))
    date=datetime.date(*date)
  except: date=None
  return date

def toDtm(s,m=0):
  # yyyy-mm-dd hh:mm:ss.123456
  # m=1 is for one second before midnight 23.59.59.999
  if not s or s=='' or s=='None': return None
  n=len(s)
  try:    
    if n==10: 
      if m==0:  time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),0,0,0,0)
      else:     time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),23,59,59,0)
    elif n==19: time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:19]),0)
    elif n==26: time=(int(s[0:4]),int(s[5:7]),int(s[8:10]),int(s[11:13]),int(s[14:16]),int(s[17:19]),int(rpad(s[20:26],6,'0')))
    date=datetime.datetime(*time)
  except: date=None
  return date

def toInt(s):
  if not s or s=='' or s=='None': return None
  try:    num=int(s)
  except: num=None
  return num

def toFlt(s):
  if not s or s=='' or s=='None': return None
  try:    num=float(s)
  except: num=None
  return num


#---- ENCRYPTION ----
def md5(data):
  return hashlib.md5(data).hexdigest()

def base26(n,f=0):
  c='abcdefghijklmnopqrstuvwxyz'
  s=''
  while n:
    m=n%26
    n=int(n/26)
    s+=c[m]
  return s[::-1].rjust(f,c[0])


#---- KEYGEN ----
# Random
# repeating:     ''.join(random.choice(chars) for _ in xrange(n))
# non-repeating  ''.join(random.sample(chars,n)) 

def randomString(n=8,chars=string.ascii_lowercase):
  return ''.join(random.choice(chars) for x in xrange(n))

def newKey(n=8):
  return ''.join(random.choice(string.ascii_lowercase) for x in xrange(n))

def newSerial():
  ep=int(time.time())
  rd=random.randint(676,17575)  # 26^2 to 26^3
  k1=base26(ep)
  k2=base26(rd)
  return k1+k2

def idify(txt,n=None):
  if not txt: return ''
  txt = re.sub(r'[^a-zA-Z]','',txt).lower()
  if n: txt=txt[:n]
  return txt

def idifynum(txt,n=None,m=3):
  if not txt: return ''
  txt = re.sub(r'[^a-zA-Z]','',txt).lower()
  if n: txt=txt[:n]
  txt=txt+(''.join(random.choice(string.digits) for x in xrange(10)))
  return txt


#---- DATES ----
def now(dateonly=0):
  if dateonly: return datetime.date.today()
  else: return datetime.datetime.now()

def today(dateonly=0):
  if dateonly: return datetime.date.today()
  else: return datetime.datetime.now()

def tomorrow(dateonly=0):
  if dateonly: return datetime.date.today()+datetime.timedelta(days=1)
  else: return datetime.datetime.now()+datetime.timedelta(days=1)

def yesterday(dateonly=0):
  if dateonly: return datetime.date.today()-datetime.timedelta(days=1)
  else: return datetime.datetime.now()-datetime.timedelta(days=1)


#---- MAIL ----
def sendMail(receiver,subject,message):
  if not mail.is_email_valid(receiver): return
  if not subject: subject='[ No subject ]'
  if not message: message='[ No message ]'
  sender=app.config.admin # sender must always be admin@example.com
  mail.send_mail(sender=sender,to=receiver,subject=subject,body=message)

def sendMailHtml(receiver,subject,body,html):
  if not mail.is_email_valid(receiver): return
  if not subject: subject='[ No subject ]'
  if not body: body='[ No message ]'
  if not html: html='[ No message ]'
  sender=app.config.admin # sender must always be admin@example.com
  mail.send_mail(sender=sender,to=receiver,subject=subject,body=body,html=html)

def sendMailAdmin(subject,message):
  sender=app.config.admin # sender must always be admin@example.com
  mail.send_mail_to_admins(sender=sender,subject=subject,body=message)


#---- IMAGES ----
def makeThumb(bits):
  #TODO: make thumbnail
  return None

def getImageInfo(data):
  # import StringIO,struct
  data = str(data)
  size = len(data)
  width  = -1
  height = -1
  content_type = ''

  # handle GIFs
  if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
    # Check to see if content_type is correct
    content_type = 'image/gif'
    w, h = struct.unpack("<HH", data[6:10])
    width = int(w)
    height = int(h)

  # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
  # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
  # and finally the 4-byte width, height
  elif ((size >= 24) and data.startswith('\211PNG\r\n\032\n') and (data[12:16] == 'IHDR')):
    content_type = 'image/png'
    w, h = struct.unpack(">LL", data[16:24])
    width = int(w)
    height = int(h)

  # Maybe this is for an older PNG version.
  elif (size >= 16) and data.startswith('\211PNG\r\n\032\n'):
    # Check to see if we have the right content type
    content_type = 'image/png'
    w, h = struct.unpack(">LL", data[8:16])
    width = int(w)
    height = int(h)

  # handle JPEGs
  elif (size >= 2) and data.startswith('\377\330'):
    content_type = 'image/jpeg'
    jpeg = StringIO.StringIO(data)
    jpeg.read(2)
    b = jpeg.read(1)
    try:
      while (b and ord(b) != 0xDA):
        while (ord(b) != 0xFF): b = jpeg.read(1)
        while (ord(b) == 0xFF): b = jpeg.read(1)
        if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
          jpeg.read(3)
          h, w = struct.unpack(">HH", jpeg.read(4))
          break
        else:
          jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
        b = jpeg.read(1)
      width = int(w)
      height = int(h)
    except struct.error:
      pass
    except ValueError:
      pass

  return content_type, width, height


#---- FILES ----
def getExtension(name):
  ext=''
  n=name.rfind('.')
  if n>-1: ext=name[n+1:]
  return ext

def getMimetype(type):
  if   type=='html': mime='text/html'
  elif type=='css' : mime='text/css'
  elif type=='js'  : mime='application/javascript'
  elif type=='img' : mime='image'
  return mime


#---- STRING ----
def replace_all(txt,dic):
  pat="(%s)"%"|".join(map(re.escape,dic.keys()))
  return re.sub(pat,lambda m:dic[m.group()],txt)

def replace_latin(txt):
  lat = 'ÁÉÍÓÚáéíóúÀÈÌÒÙàèìòùÑñÜüÇçâêîôû'
  asc = 'AEIOUaeiouAEIOUaeiouNnUuCcaeiou'
  dic = dict(zip(lat,asc))
  return replace_all(txt,dic)


#-------- END --------
