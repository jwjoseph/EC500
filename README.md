# EC500 PCR Hero
This is the project! Exciting, isn't it?

###Dependencies

The application has the following dependencies (feel free to use a virtual environment):

Python3 (3.4 and above should be good, latest preferable)

bottle for Python

pymongo for Python

MongoDB

The environment I ran this on was an Amazon Web Services (AWS) Ubuntu server (of the free variety).

## Filesystem setup
The filesystem was arranged as follows:
/home/ubuntu/pythonproject/   <-- base directory, contains the server file, libraries file, and .tpls

/home/ubuntu/pythonproject/apps/

/home/ubuntu/pythonproject/awardedbadges/

/home/ubuntu/pythonproject/badges/

/home/ubuntu/pythonproject/images/

/home/ubuntu/pythonproject/issuers/

/home/ubuntu/pythonproject/criteria/

/home/ubuntu/pythonproject/static/

/home/ubuntu/pythonproject/users/

There is absolutely nothing special about this file structure; apart from a few references that I have likely neglected to link to CONSTANT variables at the begining, you may substitute another base directory ad libitum. 

###MongoDB setup
You will need to set up a database (pcrhero) and collections (apps, badges, issuers, tasks, users).

