from fabric.api import run

from core.base import BasicTask


class InstallFirewalld(BasicTask):

    def __init__(self):
        super(InstallFirewalld, self).__init__()

    def install(self):
        run('yum install -y firewalld', quiet=True)
        run('systemctl enable firewalld')
        run('systemctl restart firewalld')

    def configure(self):
        run('firewall-cmd --permanent --zone=public --add-port=80/tcp')
        run('firewall-cmd --permanent --zone=public --add-port=443/tcp')
        run('firewall-cmd --permanent --zone=public --add-port=6379/tcp')
        run('firewall-cmd --permanent --zone=public --add-port=6432/tcp')
        run('systemctl restart firewalld')
