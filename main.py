import webapp2
import tweepy
import time

from tweepy import *

from google.appengine.ext import ndb


registerform="""
<link rel="stylesheet" href="css/style.css">
<form action="/saveregister" class="login">
	<text type="label" class="login-help">Email</text>
	<input type="email" name="remail" class="login-input">
	<text type="label" class="login-help">Password</text>
	<input type="password" name="rpwd" class="login-input">
	<input type="submit" value="Register" class="login-submit">
</form>
"""

loginform="""
<link rel="stylesheet" href="css/style.css">
<form action="/verifylogin" class="login">
	<text type="label" class="login-help">Email</text>
	<input type="email" name="lemail" class="login-input" value="email@example.com">
	<text type="label" class="login-help">Password</text>
	<input type="password" name="lpwd" class="login-input" value="password">
	<input type="submit" value="Login" class="login-submit">
</form>
"""


form="""
<link rel="stylesheet" href="css/style.css">
<form action="/postform" class="login">
	<input name="q" class="login-input">
	<input type="submit" value="Post Tweet" class="login-submit">
</form>
"""

twitterfeed="""
<div class="login">
<a class="twitter-timeline" href="https://twitter.com/gvtweetsuite" data-widget-id="574700036770152448">Tweets by @gvtweetsuite</a>
<script>!function(d,s,id){var js,fjs=d.getElementsByTagName(s)[0],p=/^http:/.test(d.location)?'http':'https';if(!d.getElementById(id)){js=d.createElement(s);js.id=id;js.src=p+"://platform.twitter.com/widgets.js";fjs.parentNode.insertBefore(js,fjs);}}(document,"script","twitter-wjs");</script>
</div>
"""

class Account(ndb.Model):
  email = ndb.StringProperty()
  password = ndb.StringProperty()

#sandy = Account(email='sandy@gmail.com', 'hello',1)
#sandy_key = sandy.put()
#sandy = sandy_key.get()

#sandy = key.get()
#sandy.email = 'sandy@gmail.co.uk'
#sandy.put()

#sandy.key.delete()

class RegisterPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(registerform)


class SaveRegister(webapp2.RequestHandler):
    def get(self):
        remail = self.request.get("remail")
        rpwd = self.request.get("rpwd")
        if not remail:
            self.redirect('/register')
        if remail:
            self.account = Account(email=remail, password=rpwd)
            self.account.put()
            self.redirect('/login')

class LoginPage(webapp2.RequestHandler):
    def get(self):
        self.response.write(loginform)



class VerifyLogin(webapp2.RequestHandler):
    def get(self):
        lemail = self.request.get("lemail")
        lpwd = self.request.get("lpwd")
        #self.account = Account(email=lemail, password=lpwd)
        qry = Account.query(Account.email == lemail).fetch()
        self.response.write(qry)
        self.response.write('<hr>')
        if not qry:
            self.redirect('/login')
        if qry:
            self.redirect('/')
        # if qry[0].email == lemail:
            # self.response.write('<p> entry found '+qry[0].email+'-->'+qry[0].password+'==> login successful </p>')
        # else:
            # self.response.write('<p> entry NOT FOUND </p>')
        #self.redirect('/')

class MainPage(webapp2.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        self.response.write(form)
        self.response.write(twitterfeed)

class PostHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get("q")
        tweet(q);
        #self.response.out.write(q + ' --> is posted to your Twitter profile!')
        self.response.write(form)
        time.sleep(10)
        self.response.write(twitterfeed)

# Update the Twitter account authorized  
# in settings.cfg with a status message.
def tweet(status):
    # http://dev.twitter.com/apps/myappid
    CONSUMER_KEY = 'mpIuWJYkQKUvaiS4FPwQpGVr8'
    CONSUMER_SECRET = 'EWOz9A9om3tf85XsF89KbIVC5LUkHEZNhdy2PcHTfOr9tP4jjE'
    # http://dev.twitter.com/apps/myappid/my_token
    ACCESS_TOKEN_KEY = '3080403725-gleW4H38K4tJ69vtUFJDZgBCr2VtqFb3D06Xk7y'
    ACCESS_TOKEN_SECRET = 'zWxk43qe3c8QlP6Pua2A81UvDTlpe90lqUVC5PxZEzcqg'

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    result = api.update_status(status)

application = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/register', RegisterPage),
    ('/saveregister', SaveRegister),
    ('/login', LoginPage),
    ('/verifylogin', VerifyLogin),
    ('/postform', PostHandler),
], debug=True)