import sys, os, bottle

sys.path = ['/var/www/termo/'] + sys.path
os.chdir(os.path.dirname(__file__))

import termo # This loads your application

application = bottle.default_app()
