#!/usr/bin/python
from fabric.api import *


def deploy():
    code_dir = '/var/opt/Shutdown-delay'
    with settings(warn_only=True):
        if run("test -d {0}".format(code_dir)).failed:
            run("git clone git@github.com:timtheonly/Shutdown-delay.git {0}".format(code_dir))
    with cd(code_dir):
        run('git pull')
