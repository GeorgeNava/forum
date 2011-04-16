from forum import app,admin

root   = app.root
routes = [
    (root+'/admin'         , admin.Panel),
    (root+'/admin/load'    , admin.Load),
    (root+'/admin/setup'   , admin.Forum),
    (root+'/admin/messages', admin.Messages),
    (root+'/admin/moderate', admin.Moderate),
]

def main(): app.control(routes)
if __name__ == '__main__': main()
