import datetime
from google.appengine.ext import webapp
 
DAYS  =['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
MONTHS=['January','February','March','April','May','June','July','August','September','October','November','December']

def longdate(dt):
  yy=dt.year
  mm=dt.month
  dd=dt.day
  ww=dt.weekday()
  hh=dt.hour
  if hh>12: hh=hh-12
  mi=str(dt.minute).zfill(2)
  am= 'am' if dt.hour<12 else 'pm'
  tt='%s, %s %s %s, %s:%s %s'%(DAYS[ww],MONTHS[mm-1],dd,yy,hh,mi,am)
  return tt

def minitime(dt):
  yy=dt.year
  mm=str(dt.month).zfill(2)
  dd=str(dt.day).zfill(2)
  hh=dt.hour
  if hh>12: hh=hh-12
  mi=dt.minute
  am= 'am' if dt.hour<12 else 'pm'
  tt='%s/%s/%s <small>%s:%s %s</small>'%(yy,mm,dd,hh,mi,am)
  return tt

def ellipsis(txt,n=80):
  m=len(txt)
  if m<n: return txt
  else: return txt[:n]+'&hellip;'

def ellipcen(txt,n=20):
  m=len(txt)
  if m<n: return txt
  else: return txt[:8]+'&hellip;'+txt[-8:]

def timeago(dt):
  if not dt: return 'Never'
  now   = datetime.datetime.now()
  delta = now-dt
  if delta.days>0:
    if delta.days>3: 
      return dt.strftime('%a, %B %d %Y %I:%M%p')
    else: 
      if delta.days==1: return 'Yesterday'
      else: return '%s days ago'%(delta.days)
  if delta.seconds>59:
    m=delta.seconds/60
    if m>59:
      h=delta.seconds/3600
      s='s' if h>1 else ''
      return '%s hour%s ago'%(h,s)
    s='s' if m>1 else ''
    return '%s minute%s ago'%(m,s)
  s='s' if delta.seconds>1 else ''
  return '%s second%s ago'%(delta.seconds,s)
 

register = webapp.template.create_template_register()
register.filter(longdate)
register.filter(minitime)
register.filter(ellipsis)
register.filter(ellipcen)
register.filter(timeago)
