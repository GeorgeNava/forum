from forum import app,views

routes = [
  (app.root+''               , views.Forum),
  (app.root+'/'              , views.Forum),
  (app.root+'/myprofile'     , views.MyProfile),
  (app.root+'/profile/(.*)'  , views.Profiles),
  (app.root+'/images/(.*)'   , views.ImageHandler),
  (app.root+'/notfound'      , views.NotFound),
  (app.root+'/newtopic/(.*)' , views.NewTopic),
  (app.root+'/(.*)/(.*)'     , views.Messages),
  (app.root+'/(.*)'          , views.Topics),
  (app.root+'.*'             , views.NotFound)
]

def main(): app.control(routes)
if __name__ == '__main__': main()
