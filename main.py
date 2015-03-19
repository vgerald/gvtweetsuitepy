import webapp2
import tweepy
import time

from tweepy import *

from google.appengine.ext import ndb

import os
import urllib
import cgi
import jinja2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class HTMLPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'email': 'Gerald@email.com',
            'title': 'Quantum Solutions: TweetSuite - Home',
        }

        template = JINJA_ENVIRONMENT.get_template('open.html')
        self.response.write(template.render(template_values))



registerform="""
<link rel="stylesheet" href="bootstrap-3.3.4/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="bootstrap-3.3.4/dist/css/signin.css">
<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <ul class="nav navbar-nav">
  <li><a href="" class="navbar-brand">
<img src="img/logo.png"></a></li>
  <li><a href="/" class="active">Home</a></li>
  <li><a href="/login">Login</a></li>
  <li><a href="/register">Register</a></li>
  <li><a href="/open">Contact</a></li>
  </ul>
</nav>

<div class="container">
<div class="form-signin">
<form action="/saveregister" class="col-lg-2">
	<span class="help-inline">Email</span>  
	<input type="email" name="remail" class="span3">
	<span class="help-inline">Password</span>  
	<input type="password" name="rpwd" class="span3">
	<input type="submit" value="Register" class="btn btn-lg btn-primary ">
</form>
</div>
</div>
"""

loginform="""
<link rel="stylesheet" href="bootstrap-3.3.4/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="bootstrap-3.3.4/dist/css/signin.css">
<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <ul class="nav navbar-nav">
  <li><a href="" class="navbar-brand">
<img src="img/logo.png"></a></li>
  <li><a href="/" class="active">Home</a></li>
  <li><a href="/login">Login</a></li>
  <li><a href="/register">Register</a></li>
  <li><a href="/open">Contact</a></li>
  </ul>
</nav>
<div class="container">
<div class="form-signin">
<form action="/verifylogin" class="col-lg-2">
	<span class="help-inline">Email</span>  
	<input type="email" name="lemail" class="span3" value="email@example.com">
	<span class="help-inline">Password</span>  
	<input type="password" name="lpwd" class="span3">
	<input type="submit" value="Login" class="btn btn-lg btn-primary ">
</form>
</div>
</div>
"""


form="""
<link rel="stylesheet" href="bootstrap-3.3.4/dist/css/bootstrap.min.css">
<link rel="stylesheet" href="bootstrap-3.3.4/dist/css/signin.css">
<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
  <ul class="nav navbar-nav">
  <li><a href="" class="navbar-brand">
<img src="img/logo.png"></a></li>
  <li><a href="/" class="active">Home</a></li>
  <li><a href="/login">Login</a></li>
  <li><a href="/register">Register</a></li>
  <li><a href="/open">Contact</a></li>
  </ul>
</nav>

<div class="container">
<form action="/postform" class="col-lg-2">
	<div class="help-inline">.</div>  
	<div class="help-inline">.</div>  
    <input type="text" name="q" class="span3">
    <input type="submit" value="Post Tweet" class="btn btn-lg btn-primary">
</form>
</div>
"""

twitterfeed="""
<div >
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
    ('/open', HTMLPage),
], debug=True)