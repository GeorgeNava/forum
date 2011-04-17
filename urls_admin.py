from forum import app,admin

routes = [
  (app.root+'/admin'         , admin.Panel),
  (app.root+'/admin/load'    , admin.Load),
  (app.root+'/admin/setup'   , admin.Forum),
  (app.root+'/admin/users'   , admin.Users),
  (app.root+'/admin/topics'  , admin.Topics),
  (app.root+'/admin/messages', admin.Messages),
]

def main(): app.control(routes)
if __name__ == '__main__': main()
