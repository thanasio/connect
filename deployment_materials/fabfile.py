import os, json
from tempfile import mkdtemp
from contextlib import contextmanager

from fabric.operations import put
from fabric.api import env, local, sudo, run, cd, prefix, task, settings, execute
from fabric.colors import green as _green, yellow as _yellow
from fabric.context_managers import hide, show, lcd
import boto
import boto.ec2
from config import Config
import time

# import configuration variables from untracked config file
aws_cfg = Config(open("aws.cfg"))
env.key_filename = os.path.expanduser(os.path.join(aws_cfg["key_dir"],
                                                   aws_cfg["key_name"] + ".pem"))


from boto import ec2

from fabric.colors import green as _green, yellow as _yellow


class EC2Conn:
    def __init__(self):
        print(_green("Started..."))
        self.ec2conn = None
        self.user = 'ubuntu'
        self.access_key = aws_cfg['aws_access_key_id']
        self.secret_key = aws_cfg['aws_secret_access_key']

    def connect(self):
        print(_green("Connecting..."))
        ec2.connect_to_region("eu-west-1a")
        self.ec2conn = ec2.connect_to_region('eu-west-1',
                  aws_access_key_id=self.access_key,
                  aws_secret_access_key=self.secret_key)


        print(self.get_instances())


    def get_instances(self):
        return self.ec2conn.get_all_instances()


def run_me():
    a = EC2Conn()
    a.connect()

#-----FABRIC TASKS-----------

def set_env_context(name):
    user = "ubuntu"
    f = open("fab_hosts/{}.txt".format(name))
    host = "54.228.139.57" #f.readline().strip()
    f.close()
    port = 22
    env.user = user
    env.hosts = ["54.228.139.57",]
    env.host_string = "{}@{} -p {}".format(user, host, port)
    print env.host_string

@task
def deploy(prod=False):
    """
    deploy the app the on the staging or production server

    :return:
    """
    if prod:
        name = "production"
    else:
        name = "staging"
    print(_green("--DEPLOYING to {}--".format(name)))
    #run_me()
    set_env_context(name)
    code_path = '/srv/kano_konnect/current'
    with cd(code_path):
        run('echo 3')
        #run('git pull')


#----------HELPER FUNCTIONS-----------

@contextmanager
def _virtualenv():
    with prefix(env.activate):
        yield