from google.appengine.ext import ndb

class Account(ndb.Model):
  email = ndb.StringProperty()
  password = ndb.StringProperty()
  logintimes = ndb.IntegerProperty()


sandy = Account(email='sandy@gmail.com', 'hello',1)
sandy_key = sandy.put()

sandy = sandy_key.get()

sandy = key.get()
sandy.email = 'sandy@gmail.co.uk'
sandy.put()


sandy.key.delete()