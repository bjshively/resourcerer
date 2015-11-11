# Resourcerer
## Summary
Resourcerer is a simple resource leasing framework, designed to allow engineers to quickly and easily secure access to the infrastructure resources needed to complete their work.

Examples of resources that may be tracked in Resourcerer include:
  - Servers
  - Storage
  - Other hardware assets

## Access
Resourcer is currently hosted at [bjshivelyuber.appspot.com](http://bjshivelyuber.appspot.com). You can sign into the system using any Google account.

## Use
Upon signing in, you will be presented with a list of available resources. Each resource will include a link to create a temporary "lease", which grants you access to the resource for a specified period of time.

In the MyLeases section of the app users can see all of their active leases, including access details for each resource. The bottom of the MyLeases view also includes a summary of all expired leases.

*Note: For demonstration purposes, all leases in this prototype environment are limited to 5 minutes in length. In a production deployment, a resource manager would specify the length of leases based on supply/demand as well as cost of resource.*

## Models
Resourcerer relies on two primary models - Resources and Leases. Below are a list of the attributes r

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
