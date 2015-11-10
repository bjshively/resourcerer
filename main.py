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


def render_template(handler, templatename, template_values):
    logout = users.create_logout_url('/')
    template_values['logout'] = logout
    path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
    html = template.render(path, template_values)
    handler.response.out.write(html)

######################################################################
# Page handlers
######################################################################


class MainPage(webapp2.RequestHandler):

    def get(self):

        Lease.check_leases()

        user = users.get_current_user()
        login = users.create_login_url('/')
        logout = users.create_logout_url('/')
        resources = Resource.get_available_resources()
        homeurl = webapp2.uri_for('home')

        template_values = {
            'user': user,
            'login': login,
            'resources': resources,
            'homeurl': homeurl,
        }

        render_template(self, 'index.html', template_values)


class CreateLease(webapp2.RequestHandler):

    def get(self, resourceid):
        resource = Resource.get_by_id(int(resourceid))
        template_values = {
            'resource': resource,
            'resourceid': resourceid
        }

        render_template(self, 'createlease.html', template_values)


class SaveLease(webapp2.RequestHandler):

    def post(self):
        r = Resource.get_by_id(int(self.request.get('resourceid')))
        r.availability = 'leased'
        r.put()

        l = Lease()
        l.populate(owner=users.get_current_user().user_id(),
                   resource=r.key,
                   expiration=Lease.get_expiration_time(),
                   active=True)
        l.put()
        
        # self.response.write(r)
        # self.response.write(l)
        template_values = {'resource': r,
                           'lease': l}
        render_template(self, 'savelease.html', template_values)


class CreateResource(webapp2.RequestHandler):

    def get(self):
        template_values = {}
        render_template(self, 'createresource.html', template_values)


class SaveResource(webapp2.RequestHandler):

    def post(self):
        r = Resource()
        r.populate(resType=self.request.get('resType'),
                   title=self.request.get('title'),
                   description=self.request.get('description'),
                   access=self.request.get('access'),
                   availability='true')
        r.put()
        self.redirect('/')

######################################################################
# DB objects
######################################################################


class Resource(ndb.Model):
    """A resource asset that can be leased by a user"""
    resType = ndb.StringProperty()
    title = ndb.StringProperty()
    description = ndb.StringProperty()
    availability = ndb.StringProperty()
    access = ndb.StringProperty()

    @classmethod
    def get_available_resources(cls):
        """Returns a list of all available resources"""
        results = cls.query(cls.availability == 'true').fetch()
        records = []
        for item in results:
            d = {}
            d['resType'] = item.resType
            d['title'] = item.title
            d['description'] = item.description
            d['access'] = item.access
            d['urlkey'] = item.key.id()
            records.append(d)
        return records


class Lease(ndb.Model):
    """A lease that grants a user access to a resource for a period of time"""
    owner = ndb.StringProperty()
    resource = ndb.KeyProperty()
    creation = ndb.DateTimeProperty(auto_now_add='True')
    expiration = ndb.DateTimeProperty()
    active = ndb.BooleanProperty()

    @classmethod
    def check_leases(cls):
        """Checks expiration of all leases and updates availability of resource for any expired lease"""
        now = datetime.now()
        leases = cls.query(cls.active == True).fetch()
        for lease in leases:
          if lease.expiration < now:
            lease.active = False
            lease.put()
            r = Resource.get_by_id(lease.resource.id())
            r.availability = 'true'
            r.put()

    @classmethod
    def get_expiration_time(cls):
        """Returns the expiration time for a lease"""
        return datetime.now() + timedelta(minutes=5)


######################################################################
# define routes and create the app
######################################################################
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='home'),
    webapp2.Route(r'/createresource', handler=CreateResource),
    webapp2.Route(r'/saveresource', handler=SaveResource),
    webapp2.Route(r'/createlease/<resourceid:\d+>', handler=CreateLease),
    webapp2.Route(r'/savelease', handler=SaveLease)],
    debug=True)
