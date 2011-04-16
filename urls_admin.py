from forum import app,admin

routes = [
  (app.root+'/admin'         , admin.Panel),
  (app.root+'/admin/load'    , admin.Load),
  (app.root+'/admin/setup'   , admin.Forum),
  (app.root+'/admin/messages', admin.Messages),
  (app.root+'/admin/moderate', admin.Moderate),
]

def main(): app.control(routes)
if __name__ == '__main__': main()
