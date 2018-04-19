import os

from decouple import Csv, config
from fabric.api import env

from core.update import UpdateOS
from tasks.firewalld import InstallFirewalld
from tasks.miniconda import InstallMiniconda
from tasks.nginx import InstallNginx
from tasks.pgbouncer import InstallPgBouncer
from tasks.postgresql import InstallPostgreSQL
from tasks.redis import InstallRedis

env.hosts = config('CLOUD_HOSTS', cast=Csv())
env.port = config('CLOUD_PORT', cast=int)
env.user = config('CLOUD_USER')
env.password = os.environ.get('CLOUD_PASSWORD')


def update_os():
    update = UpdateOS()
    update.update_os()


def postgresql():
    task = InstallPostgreSQL()
    task.install()
    task.configure()


def pgbouncer():
    task = InstallPgBouncer()
    task.install()
    task.configure()


def firewalld():
    task = InstallFirewalld()
    task.install()
    task.configure()


def nginx():
    task = InstallNginx()
    task.install()
    task.configure()


def redis():
    task = InstallRedis()
    task.install()
    task.configure()


def miniconda():
    task = InstallMiniconda()
    task.install()
    task.configure()


def setup_complete():
    update_os()
    postgresql()
    pgbouncer()
    firewalld()
    nginx()
    redis()
    miniconda()
