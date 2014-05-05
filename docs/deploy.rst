Deploy
======

Infrastructure Overview
-----------------------

The Kano-Konnect project runs in production on an EC2 micro instance
in the EU-west-1 Availability zone. At present, the EC2 instance is named
"kano-konnect-webserver".

The EC2 instance is part of a security group that exposes port 80 to
the open internet. The deployment uses nginx as a reverse proxy to
listen on port 80 and route requests from the open internet into a
uWSGI webserver. The nginx reverse proxy also directly
serves static files (images, CSS, etc.) out of a directory inside the
main project repo.

The uWSGI server runs the Django project code. We also run Celery
workers to process asynchronous tasks (with tasks and results passed
back and forth via a RabbitMQ server.)

<IN THE FUTURE>
Finally, an instance of JenkinsCI is running on the server. Jenkins
listens to a Github webhook, and when a new build is pushed to the
master repo, Jenkin runs the project test suite. If the test suite
passes, Jenkins deploys the new commit to the live production server.
</FUTURE>

Project code
------------

All project/Python code lives in the directory::

  /srv/kano_konnect

This directory contains three subdirectories:

*releases* -- where the actual Python code lives. The live code is
current inside releases/kano_konnect. But more directories can be
created here to allow testing of new major releases while still
enabling rapid rollback.

*shared* -- where any files that will be common to all releases should
live. Currently, that mainly means the project virtualenv which is
located at /srv/kano_konnect/shared/env

*current* -- a symlink to the current, production code. 


Static files
************

Static files are served directly off the server from a directory via
nginx (see below.)

For ease of use, I track all the statics in Github and simply
push/pull them to the server. So the static directory is inside the
project repo (currently at
/srv/kano_konnect/current/kano_konnect/assets/).  

This may not be best practice overall (git is not ideal for non-text
files like images) but in my experience it works fine up to at least
~100mb of static assets. And it makes the deployment process much
simpler. Just make sure to run::

  python manage.py collectstatic

Before pushing commits to Github.

Requirements
************

Updating the virtualenv is not yet automated. So if you add new
packages to the project, you must install them manually. Do do this,
run:::

  source /srv/kano_konnect/shared/env/bin/activate
  pip install *your package or requirements file*


NGINX
-----

The nginx server is configured by two key config files.

The actual nginx server config is at:::

  /etc/nginx/nginx.conf

And the kano-konnect site specific configuration is at:::

  /etc/nginx/sites-available/kano_konnect.conf

(The site specific file is symlinked to
/etc/nginx/sites-enabled/kano_konnect.conf to make nginx actually
serve the site.)

The key stanzas in config files are:
************************************

In kano_konnect.conf:
&&&&&&&&&&&&&&&&&&&&&

**location /static/ must point to the directory where static files live
on the server (currently the "assets" directory).**

Before pushing a commit to Github, you should collect static files
(which will put everything into the assets directory.) Then when you
pull on the server, the static assets will be pulled from Github and
put in the right place.

**location / must point to the socket or port that uUWGI is listening
on.**

Currently I have uWSGI running on port 9090. It may be somewhat
faster to run on a unix socket but for a low traffic site the
difference is likely to be immaterial. I'll leave it as it is for now
because it currently works fine.

This can easily be changed if you have a preferred way to run uWSGI.

In nginx.conf:
&&&&&&&&&&&&&&

The project repo is owned by the "nobody user" so nginx must run as
"nobody". This is accomplished by adding the line:::

  user nobody nogroup;

To nginx.conf

Supervisor
-----

The uWSGI process (and also Celery -- see below) is managed by
supervisor, a python process controller that gives a convenient way to
keep the server process alive by restarting it if it crashes for some
reason.

Supervisor also gives a way to start/restart the uWSGI process from
the commandline via the *supervisorctl* command, e.g.::

  sudo supervisorctl restart kano_konnect-uwsgi

Supervisor needs to be told how to start the uWSGI and celery
processes, and those instructions live at:::

  /etc/supervisor.d/kano_konnect-uwsgi.conf

and::
  
  /etc/supervisor.d/kano_konnect-celeryd.conf


The key line in these files is:::
  
  command=/srv/kano_konnect/shared/env/bin/uwsgi --http :9090 --wsgi-file kano_konnect/kano_konnect/wsgi.py

This line must specify exactly how the process would be started from
the commandline. If you wish to change uWSGI to use a Unix socket (or
an .ini file), you'll need to edit this line.

By default, supervisor routes all log output to the directory::

  /var/log/supervisor/

And creates one log file for the stdout and stderr of each managed
process.

If you edit supervisor config files, you must "reread" them with the
command:::
  
  sudo supervisorctl reread

And then reload supervisor with:::
  
  sudo supervisorctl reload

You can also restart supervised processes with::
  
  sudo supervisorctl restart [PROCESS_NAME]


uWSGI
-----

The uWSGI configuration is currently very "off the shelf". No .ini
file is being used. If you wish to supply a .ini file, write one and
edit the supervisor config file for uWSGi to include it via the
command line command.

Celery
------

Celery is also managed by supervisor. The integration into Django is
specified in the file::

  /srv/kano_konnect/current/kano_konnect/kano_konnect/celery.py

Tasks should be specified inside of the file:::

  /srv/kano_konnect/current/kano_konnect/kano_konnect/tasks.py

On the server, Celery requires rabbitmq to be running. Rabbit should
start when the server starts and run automatically, but if it ever
crashes it can be restarted with:::
  
  sudo service rabbitmq-server restart

Postgres
--------

Postgres is running as a service on the webserver. The "cluster"
contains a database called "kano_konnect". You can interact
via psql by doing::

  sudo -u postgres psql


Updating code:
--------------

The CI integration is currently broken. So code must be updated
manually.

To update the repo, simply ssh into the server via something like::

  ssh -i ~/.ec2/kano-konnect-key.pem ubuntu@ec2-54-228-139-57.eu-west-1.compute.amazonaws.com

Then do::

  cd /srv/kano_konnect/current
  sudo -u nobody git pull
  source /srv/kano_konnect/shared/env/bin/activate
  cd kano_konnect/
  # sync the database
  sudo -u nobody python manage.py syncdb --settings=kano_konnect.settings.production
