Deploy
========

# Infrastructure Overview

The Kano-Konnect project runs in production on an EC2 micro instance
in the EU-1 Availability zone. At present, the EC2 server is named
"kano-konnect-webserver".

The EC2 instance is part of a security group that exposes port 80 to
the open internet. The deployment uses nginx as a reverse proxy to
listen on port 80 and route requests from the open internet into a
uWSGI webserver. The nginx reverse proxy is also used to directly
serve static files (images, CSS, etc.)

The uWSGI server runs the Django project code. The Django project
also uses Celery workers to process asynchronous tasks (with tasks and
results passed back and forth via a RabbitMQ server.)

Finally, an instance of JenkinsCI is running on the server. Jenkins
listens to a Github webhook, and when a new build is pushed to the
master repo, Jenkin runs the project test suite. If the test suite
passes, Jenkins deploys the new commit to the live production server.




