from decouple import config
from fabric.api import run


class UpdateOS:

    def __init__(self):
        timezone = config('CLOUD_TIMEZONE')
        run(f'timedatectl set-timezone {timezone}')

    def update_os(self):
        run('yum localinstall -y --nogpgcheck https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.\
noarch.rpm https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-7.noarch.rpm', quiet=True)
        run('yum update -y')
        run('yum install -y bash-completion yum-utils sysstat net-tools gcc vim git openssl openssl-devel htop wget')
