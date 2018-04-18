from fabric.api import run
from fabric.contrib import files

from core.base import BasicTask


class InstallNginx(BasicTask):

    def __init__(self):
        super(InstallNginx, self).__init__()

    def install(self):
        if not files.exists('/etc/nginx'):
            run('yum install -y nginx', quiet=True)
            run('systemctl enable nginx')

        run('systemctl restart nginx')

    def configure(self):
        # run('firewall-cmd --permanent --zone=public --add-port=80/tcp')
        # run('firewall-cmd --permanent --zone=public --add-port=443/tcp')
        # run('firewall-cmd --permanent --zone=public --add-port=6432/tcp')
        # run('systemctl restart firewalld')
        pass
