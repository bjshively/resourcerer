import os
import time
import webapp2

from datetime import datetime, timedelta
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from webapp2_extras import routes

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
        resources = Resource.get_available_resources()
        homeurl = webapp2.uri_for('home')
        test = Resource.get_by_id(5910974510923776)

        template_values = {
            'user': user,
            'login': login,
            'logout': logout,
            'resources': resources,
            'homeurl': homeurl,
            'test': test
        }

        """
    res = Resource()
    res.resType = 'Server'
    res.title = 'DonkeyKong'
    res.description = 'An Ubuntu 14.04 server for all your computing needs.'
    res.availability = 'true'
    res.put()
    """
        render_template(self, 'index.html', template_values)


class CreateLease(webapp2.RequestHandler):

    def get(self, resourceid):
        resource = Resource.get_by_id(int(resourceid))

        template_values = {
            'resource': resource
        }

        render_template(self, 'createlease.html', template_values)


class SaveLease(webapp2.RequestHandler):

    def post(self):
        return 1

######################################################################
# DB objects
######################################################################

class Resource(ndb.Model):
    """A resource asset that can be leased by a user"""
    resType = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    availability = ndb.StringProperty()

    @classmethod
    def get_available_resources(cls):
        """Returns a list of all available resources"""
        results = cls.query(cls.availability == 'true').fetch()
        records = []
        for item in results:
            d = {}
            d['title'] = item.title
            d['description'] = item.description
            d['resType'] = item.resType
            d['urlkey'] = item.key.id()
            records.append(d)
        return records


class Lease(ndb.Model):
    """A lease that grants a user access to a resource for a period of time"""
    owner = ndb.UserProperty()
    resource = ndb.KeyProperty()
    creation = ndb.DateTimeProperty(auto_now_add='True')
    expiration = ndb.DateTimeProperty()

    @classmethod
    def get_expiration_time(cls):
        """Returns the expiration time for a lease"""
        return datetime.now() + timedelta(hours=2)

######################################################################
# define routes and create the app
######################################################################
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='home'),
    webapp2.Route(r'/createlease/<resourceid:\d+>', handler=CreateLease)],
    debug=True)
