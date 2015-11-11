import os
import time
import webapp2

from datetime import datetime, timedelta
from google.appengine.api import mail
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from webapp2_extras import routes

######################################################################
# Helper functions
######################################################################

def render_template(handler, templatename, template_values):
    """Render RequestHandler page template with the specified values"""
    # Insert base template values
    logout = users.create_logout_url('/')
    login = users.create_login_url('/')
    user = users.get_current_user()

    homelink = webapp2.uri_for('home')
    myleaseslink = webapp2.uri_for('myleases')
    leaselink = webapp2.uri_for('viewlease')

    template_values['logout'] = logout
    template_values['login'] = login
    template_values['homelink'] = homelink
    template_values['myleaseslink'] = myleaseslink
    template_values['leaselink'] = leaselink
    template_values['user'] = user

    path = os.path.join(os.path.dirname(__file__), 'templates/' + templatename)
    html = template.render(path, template_values)
    handler.response.out.write(html)

def check_login(handler):
    if not (users.get_current_user()):
        handler.redirect('/')

######################################################################
# Page handlers
######################################################################


class MainPage(webapp2.RequestHandler):
    """View that lists currently available resources"""

    def get(self):

        Lease.check_leases()
        resources = Resource.get_available_resources()

        template_values = {
            'resources': resources
        }

        render_template(self, 'index.html', template_values)


class MyLeases(webapp2.RequestHandler):

    def get(self):
        Lease.check_leases()
        check_login(self)
        
        userid = users.get_current_user().user_id()
        leaseResults = Lease.query(Lease.owner == userid).order(-Lease.creation).fetch()
        leases = []
        expiredLeases = []

        for lease in leaseResults:
            l = lease.to_dict()
            resource = Resource.get_by_id(lease.resource.id())
            l['resourceTitle'] = resource.title
            l['resourceAccess'] = resource.access

            if lease.active:
                leases.append(l)
            else:
                expiredLeases.append(l)
        template_values = {
            'leases': leases,
            'expiredLeases': expiredLeases
        }

        render_template(self, 'myleases.html', template_values)


class LeasePage(webapp2.RequestHandler):

    def get(self, resourceid):
        """View that confirms registering a resource lease"""
        resource = Resource.get_by_id(int(resourceid))
        template_values = {
            'resource': resource,
            'resourceid': resourceid
        }

        render_template(self, 'createlease.html', template_values)

    def post(self):
        """View that confirms lease save and provides resource access details"""
        r = Resource.get_by_id(int(self.request.get('resourceid')))
        if r.availability != 'true':
            error_message = 'The selected resource unavailable. Please try again later.'
            template_values = {'error_message': error_message}
            render_template(self, 'error.html', template_values)

        else:
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

class ViewLease(webapp2.RequestHandler):
    """View the details of a lease"""

    def get(self, leaseid):
        lease = Lease.get_by_id(int(leaseid))
        template_values = {}


class ResourcePage(webapp2.RequestHandler):
    """View to enter new resources into the system"""

    def get(self):
        check_login(self)
        template_values = {}
        render_template(self, 'createresource.html', template_values)

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
# NDB Models
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
        results = cls.query(cls.availability == 'true').order(Resource.resType).fetch()
        resources = []
        for item in results:
            d = {}
            d['resType'] = item.resType
            d['title'] = item.title
            d['description'] = item.description
            d['access'] = item.access
            d['urlkey'] = item.key.id()
            resources.append(d)
        return resources


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
# Routes & App
######################################################################
app = webapp2.WSGIApplication([
    webapp2.Route(r'/', handler=MainPage, name='home'),
    webapp2.Route(r'/myleases', handler=MyLeases, name='myleases'),
    webapp2.Route(r'/resource', handler=ResourcePage),
    webapp2.Route(r'/lease', handler=LeasePage, name='viewlease'),
    webapp2.Route(r'/lease/<resourceid:\d+>', handler=LeasePage, name='lease')],
    debug=True)
