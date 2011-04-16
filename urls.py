from forum import app,views,admin,setup

root   = app.root
routes = [
    (root+''               , views.Forum),
    (root+'/'              , views.Forum),
    (root+'/newtopic/(.*)' , views.NewTopic),
    (root+'/profile/.*'    , views.Profiles),
    (root+'/images/.*'     , views.ImageHandler),
    (root+'/notfound'      , views.NotFound),
    (root+'/(.*)/(.*)'     , views.Messages),
    (root+'/(.*)'          , views.Topics),
    (root+'/.*'            , views.NotFound)
]

def main(): app.control(routes)
if __name__ == '__main__': main()
