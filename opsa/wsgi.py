"""
WSGI config for opsa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
"""

import os
import sys

opsa_cobfiguration = os.path.dirname(__file__)
project = os.path.dirname(opsa_cobfiguration)
workspace = os.path.dirname(project)
sys.path.append(project)
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opsa.settings")

os.environ['DJANGO_SETTINGS_MODULE'] = 'opsa.settings'
#application = get_wsgi_application()
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
