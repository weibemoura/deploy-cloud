from fabric.api import run
from fabric.contrib import files

from core.base import BasicTask


class InstallRedis(BasicTask):

    def __init__(self):
        super(InstallRedis, self).__init__()

    def install(self):
        if not files.exists('/etc/redis.conf'):
            run('yum install -y redis', quiet=True)
            run('systemctl enable redis')

        run('systemctl restart redis')

    def configure(self):
        pass
