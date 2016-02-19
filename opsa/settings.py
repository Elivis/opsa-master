"""
Django settings for opsa project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')_4x-6mbf8j0j=-y)115vr^!#^^%fltpn_2(pro1no9a^_x_st'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    BASE_DIR + '/templates',
)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    #'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'opsa',
    'asset',
    'installed',
    'config',
    'api',
    'deploy',
    'UserManage',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    #'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)

ROOT_URLCONF = 'opsa.urls'

WSGI_APPLICATION = 'opsa.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'opsagit',
        'USER': 'opsagit',
        'PORT': 3306,
        'PASSWORD': 'passwd',
    }
}


LANGUAGE_CODE = 'zh-CN'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'

STATICFILES_DIRS = (
    BASE_DIR + '/static',
)

try:
    from settings_local import *
except ImportError:
    pass

'''
#ldap

import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType


# Baseline configuration.
AUTH_LDAP_SERVER_URI = "ldap://domain.net:389"
AUTH_LDAP_CONNECTION_OPTIONS = { 
  ldap.OPT_REFERRALS: 0
}

AUTH_LDAP_BIND_DN = "CN=app,CN=Users,DC=domain,DC=net"               
AUTH_LDAP_BIND_PASSWORD = "domain@com"
AUTH_LDAP_USER_SEARCH = LDAPSearch("DC=domain,DC=net", ldap.SCOPE_SUBTREE, "(sAMAccountName=%(user)s)")
# AUTH_LDAP_USER_DN_TEMPLATE = "sAMAccountName=%(user)s,OU=Employees,OU=Cisco Users,DC=cisco,DC=com"

# Populate the Django user from the LDAP directory.
AUTH_LDAP_USER_ATTR_MAP = {
  "nickname":"displayname",
  "mobile":"mobile",
  "email": "mail",  
  "is_active": 1,
}
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
    'is_active': 'CN=Domain Users,OU=Builtin,DC=domain,DC=net',
    #'is_staff': 'CN=Users,DC=domain,DC=net',
    #'is_superuser': 'cn=superuser,OU=GlobalUsers,DC=test,DC=domain,DC=com'
}
# This is the default, but I like to be explicit.
AUTH_LDAP_ALWAYS_UPDATE_USER = True

# Use LDAP group membership to calculate group permissions.
AUTH_LDAP_FIND_GROUP_PERMS = True

# Cache group memberships for an hour to minimize LDAP traffic
AUTH_LDAP_CACHE_GROUPS = True
AUTH_LDAP_GROUP_CACHE_TIMEOUT = 3600

# Keep ModelBackend around for per-user permissions and maybe a local
# superuser.
AUTHENTICATION_BACKENDS = (
  'django_auth_ldap.backend.LDAPBackend',
  'django.contrib.auth.backends.ModelBackend',
)
'''
AUTH_USER_MODEL = 'UserManage.User'


import logging
logger = logging.getLogger('django_auth_ldap')
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#SESSION

SESSION_COOKIE_HTTPONLY = True 
CSRF_COOKIE_HTTPONLY = True
