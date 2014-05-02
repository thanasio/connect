from base import *

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


NOSE_ARGS = [
    #'--with-coverage',  # uncomment to run tests with coverage
]