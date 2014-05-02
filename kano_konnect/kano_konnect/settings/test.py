import sys
from base import *
from django.test.utils import setup_test_environment

DEBUG = True

## Apps for testing
INSTALLED_APPS = (
 'django_nose',
) + INSTALLED_APPS  # nose needs to be before South

print INSTALLED_APPS
## END apps

########## TEST SETTINGS
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

"""
NOSE_ARGS = [
    '--with-coverage',
    '--cover-inclusive',
]
"""

print "ROOO {}".format(DJANGO_ROOT)
sys.path.append(DIRECTORY_ROOT)
for paf in sys.path:
    print "PATH {}".format(paf)