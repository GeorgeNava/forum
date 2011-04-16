import app,models,forms,utils


class Panel(app.request):
  def get(self):
    data={
      'topics'  :models.latestTopics(),
      'messages':models.latestMessages(),
      'users'   :models.latestUsers()
    }
    self.show('admin',data)
  

class Forum(app.request):
  def get(self):
    data={'forums':models.getForums(),}
    self.show('admin_forum',data)
  
  def post(self):
    form = forms.newForum(self)
    if form.ok or form.redirect:
      self.redirect(form.url)
    else:
      self.show('admin_forum',form.data)

  def delete(self):
    fid=self.request.get('id')
    if fid:
      models.deleteForum(fid)
      self.write('{"ok":200}')
    else:
      self.write('{"error":"No id provided"}')


class Messages(app.request):
  def get(self):
    data={}
    self.show('admin_messages',data)
  

class Moderate(app.request):
  def get(self):
    data={}
    self.show('admin_moderate',data)
  

class Load(app.request):
  def get(self):
    models.newForum({
      'url'        :'lobby',
      'order'      :1,
      'title'      :'Lobby',
      'description':'Here you can ask any question or make any comment about the forum.'
    })
     
    models.newForum({
      'url'        :'events',
      'order'      :2,
      'title'      :'Events & Meetings',
      'description':'Lets get together, gatherings, reunions or just for beers.'
    })

    models.newForum({
      'url'        :'developers',
      'order'      :3,
      'title'      :'Developers Hack',
      'description':'Here we talk about code, programming techniques and everything hackish.'
    })

    models.newForum({
      'url'        :'designers',
      'order'      :4,
      'title'      :'Designers Den',
      'description':'Themes, colors, palettes, tips and tricks for the creative minds.'
    })
    self.redirect(app.root)

