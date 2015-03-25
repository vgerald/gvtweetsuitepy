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

class LoginPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'email': 'Gerald@email.com',
            'title': 'Quantum Solutions: TweetSuite - Login',
        }

        template = JINJA_ENVIRONMENT.get_template('login.html')
        self.response.write(template.render(template_values))
class RegisterPage(webapp2.RequestHandler):

    def get(self):
        template_values = {
            'email': 'Gerald@email.com',
            'title': 'Quantum Solutions: TweetSuite - Register',
        }

        template = JINJA_ENVIRONMENT.get_template('register.html')
        self.response.write(template.render(template_values))




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
    <div class="pull-left">
      <form class="post-tweet" action="/postform">
        <h2 class="post-tweet-heading">Enter Tweet</h2>
        <input type="text" name="q" class="form-control" placeholder="Tweet" required autofocus>
        <button class="btn btn-lg btn-primary btn-block" type="submit">Post Tweet</button>
      </form>
    </div> <!-- /pull-left -->
    </div> <!-- /container -->
"""
googlechart1="""
    <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1.1", {packages:["bar"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
	  var data = google.visualization.arrayToDataTable([
          ['TweetID', 'Retweets', 'Favorites']
"""

googlechart2="""
        var options = {
          chart: {
            title: 'Tweet Performance',
            subtitle: 'Re-tweets and Favourites of recent 10 tweets',
          },
          bars: 'horizontal' // Required for Material Bar Charts.
        };

        var chart = new google.charts.Bar(document.getElementById('barchart_material'));

        chart.draw(data, options);
      }
    </script>
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
        #self.response.write(twitterfeed)
        CONSUMER_KEY = 'mpIuWJYkQKUvaiS4FPwQpGVr8'
        CONSUMER_SECRET = 'EWOz9A9om3tf85XsF89KbIVC5LUkHEZNhdy2PcHTfOr9tP4jjE'
        # http://dev.twitter.com/apps/myappid/my_token
        ACCESS_TOKEN_KEY = '3080403725-gleW4H38K4tJ69vtUFJDZgBCr2VtqFb3D06Xk7y'
        ACCESS_TOKEN_SECRET = 'zWxk43qe3c8QlP6Pua2A81UvDTlpe90lqUVC5PxZEzcqg'

        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_TOKEN_KEY, ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth)
        pub = api.user_timeline()[:10]
        self.response.write('<em>User Timeline::</em>')
        self.response.write('<table class="table table-striped table-bordered table-condensed"><thead><tr><th>id</th><th>what</th><th>who</th><th># of retweets</th><th># of favorites</th><th>when</th></tr></thead><tbody>')
        for i in pub:
            self.response.write('<tr>')
            self.response.write('<td>' + str(i.id) + '</td>')
            self.response.write('<td>' + i.text + '</td>')
            self.response.write('<td>' + i.user.name + '</td>')
            #self.response.write('<td>' + str(i.user.followers_count) + '</td>')
            self.response.write('<td>' + str(i.retweet_count) + '</td>')
            self.response.write('<td>' + str(i.user.favourites_count) + '</td>')
            self.response.write('<td>' + str(i.created_at) + '</td>')
            self.response.write('</tr>')
        self.response.write('</tbody></table> <hr>')
        pub = api.home_timeline()[:10]
        self.response.write('<em>Home Timeline::</em>')
        self.response.write('<table class="table table-striped table-bordered table-condensed"><thead><tr><th>id</th><th>what</th><th>who</th><th># of retweets</th><th># of favorites</th><th>when</th></tr></thead><tbody>')
        for i in pub:
            self.response.write('<tr>')
            self.response.write('<td>' + str(i.id) + '</td>')
            self.response.write('<td>' + i.text + '</td>')
            self.response.write('<td>' + i.user.name + '</td>')
            #self.response.write('<td>' + str(i.user.followers_count) + '</td>')
            self.response.write('<td>' + str(i.retweet_count) + '</td>')
            self.response.write('<td>' + str(i.user.favourites_count) + '</td>')
            self.response.write('<td>' + str(i.created_at) + '</td>')
            self.response.write('</tr>')
        self.response.write('</tbody></table><hr>')
        self.response.write('<div id="barchart_material" style="width: 900px; height: 500px;"></div>')
        self.response.write(googlechart1)
        for i in pub:
            self.response.write(',')
            self.response.write('["' + str(i.id) + '",' + str(i.retweet_count) + ','+str(i.user.favourites_count)+']')
        self.response.write(']);')
        self.response.write(googlechart2)
## Get the User object for twitter...
#user = tweepy.api.get_user('twitter')
# print user.screen_name
# print user.followers_count
# for friend in user.friends():
   # print friend.screen_name

class PostHandler(webapp2.RequestHandler):
    def get(self):
        q = self.request.get("q")
        tweet(q);
        #self.response.out.write(q + ' --> is posted to your Twitter profile!')
        #time.sleep(10)
        self.redirect('/')


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