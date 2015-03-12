from google.appengine.ext import ndb

class Account(ndb.Model):
  email = ndb.StringProperty()
  password=ndb.StringProperty()
  logintimes = ndb.IntegerProperty()


sandy = Account(username='Sandy',
                userid=123,
                email='sandy@gmail.com')

				
sandy_key = sandy.put()

sandy = Account()
sandy.username = 'Sandy'
sandy.userid = 123
sandy.email = 'sandy@gmail.com'


sandy = key.get()
sandy.email = 'sandy@gmail.co.uk'
sandy.put()


sandy.key.delete()