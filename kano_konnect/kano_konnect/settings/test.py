from base import *

DEBUG = True

## Apps for testing
INSTALLED_APPS = (
 'django_nose',
 "django_jenkins",
) + INSTALLED_APPS  # nose needs to be before South

print INSTALLED_APPS
## END apps

########## TEST SETTINGS
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
SECRET_KEY = os.getenv("SECRET_KEY", "$testing_key$")

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

JENKINS_TASKS = (
    'django_jenkins.tasks.run_pylint',
    'django_jenkins.tasks.with_coverage',
)

PROJECT_APPS = LOCAL_APPS