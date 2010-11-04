from fabric.api import *

env.hosts = ['mpug-demo.roryhart.net']
#env.shell = '/bin/bash -c'

def pack():
    with cd('/tmp/'):
        local('git clone git@github.com:hartror/MPUG-Fabric-Demo.git mpug_demo')
        local('tar czf mpug_demo.tgz mpug_demo/')
        local('rm mpug_demo -rf')

def deploy():
    pack()
    put('/tmp/mpug_demo.tgz', '/tmp/')
    with cd('/tmp'):
        run('tar xof mpug_demo.tgz')
    run('rm /opt/django/mpug_demo -rf')
    run('mv /tmp/mpug_demo /opt/django/mpug_demo')
    with cd('/opt/django/mpug_demo/mpug_demo/'):
        run('mv live_settings.py settings.py')
    run('rm /tmp/mpug_demo.tgz')

def stop_fastcgi():
    run('kill `cat /opt/django/mpug_demo.pid`')

def start_fastcgi():
    run('source /opt/django/virtualenv/bin/activate && /opt/django/virtualenv/bin/python /opt/django/mpug_demo/mpug_demo/manage.py runfcgi method=prefork host=0.0.0.0 port=3033 daemonize=true pidfile=/opt/django/mpug_demo.pid')

def restart_fastcgi():
    stop_fastcgi()
    start_fastcgi()
