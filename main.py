import os
import time
import webapp2

from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template

######################################################################
# Helper function to render templates
######################################################################
def render_template(handler, templatename, templatevalues):
  path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
  html = template.render(path, templatevalues)
  handler.response.out.write(html)

######################################################################
# Page handlers
######################################################################

class MainPage(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    login = users.create_login_url('/')
    logout = users.create_logout_url('/')

    template_values = {
      'user': user,
      'login': login,
      'logout': logout
    }

    render_template(self, 'index.html', template_values)

class ErrorPage(webapp2.RequestHandler):
  def get(self):
    code = self.request.get('msg')
    error_msg = 'An unknown error occurred.'

    template_values = {
      'error_msg': error_msg
    }

    render_template(self, 'error.html', template_values)

######################################################################
# DB objects
######################################################################
class Resource(db.Model)

######################################################################
# define routes and create the app
######################################################################
app = webapp2.WSGIApplication([
  ('/', MainPage)],
  debug=True)