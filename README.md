# Resourcerer
## Summary
Resourcerer is a simple resource leasing framework, designed to allow engineers to quickly and easily secure access to the infrastructure resources needed to complete their work.

Examples of resources that may be tracked in Resourcerer include:
  - Servers
  - Storage
  - Other hardware assets

![Main View](http://bjshivelyuber.appspot.com/static/resourcerermain.png)

## Access
Resourcer is currently hosted at [bjshivelyuber.appspot.com](http://bjshivelyuber.appspot.com). You can sign into the system using any Google account.

## Usage

### Leasing
Upon signing in, you will be presented with a list of resources ordered by type. These are the resources that are currently available to lease. To lease a resource, click on the __Lease this resource__ link. You will be taken to a confirmation page. Click __Cancel__ to return home, or __Create Lease__ to reserve the resource.

![Lease Created](http://bjshivelyuber.appspot.com/static/resourcererleasecreated.png)

On the __My Leases__ page, you can see all of your active leases, as well as access details for each resource. Click on the bar icon next to __Access Details__ to reveal the details for any currently leased resource. The bottom of the MyLeases view also includes a summary of all previously expired leases.

![My Leases](http://bjshivelyuber.appspot.com/static/resourcerermyleases.png)

*Note: For demonstration purposes, all leases in this prototype environment are limited to 5 minutes in length. In a production deployment, a resource manager would specify the length of leases based on supply/demand as well as cost of resource.*

### Creating Resources
In addition to leasing resources, you can add new resources to the system, making them accessible to other users. To begin, click on __Add Resource__ in the navigation bar.

You will be given a form to select a __Resource Type__, give the resource a __Title__ and __Description__ and to share any __Access Details__ such as IP, username, password, physical location, etc. Click __Save Resource__. You will be returned to the main resource list and your addition will appear.

*Note: In the future it may make sense to define roles within the system and restrict creation of new resources to a subset of users such as Resource Managers. For now, this page is open to all users.*

## Models
Resourcerer relies on two primary models - Resources and Leases. Below are lists of the attributes contained within each of these object types.

### Resources
- resType - the type of resource
- title - the name of the resource
- description - a description of the resource
- availability - availability state, i.e. true, leased, maintenance
- access - access instructions such as IP, username, password, etc. 

### Leases
- owner - the user to which the lease is granted
- resource - the resource to which the lease applies
- creation - the time the lease was granted
- expiration - the time the lease expires
- active - flag that specifies if a lease is currently active or not

## Code
Resourcerer is written in python and runs on Google AppEngine.

It uses the following frontend libraries:
- Bootstrap
- jQuery
- FontAwesome

The source code can be viewed on [github](http://github.com/bjshively/resourcerer).

## Author
Developed by Bradley Shively

bshively@gmail.com

November 2015
