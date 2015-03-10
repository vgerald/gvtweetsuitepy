import webapp2
import tweepy
import time

from tweepy import *

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
    ('/postform', PostHandler),
], debug=True)