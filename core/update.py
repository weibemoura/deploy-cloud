from decouple import config
from fabric.api import run


class UpdateOS:

    def __init__(self):
        timezone = config('CLOUD_TIMEZONE')
        run(f'timedatectl set-timezone {timezone}')

    def update_os(self):
        link = ' '.join(self.__link_repositories())
        packages = ' '.join(self.__list_packages())

        run(f'yum localinstall -y --nogpgcheck {link}')
        run('yum update -y')
        run(f'yum install -y {packages}')

    def __link_repositories(self):
        return [
            'https://download1.rpmfusion.org/free/el/rpmfusion-free-release-7.noarch.rpm',
            'https://download1.rpmfusion.org/nonfree/el/rpmfusion-nonfree-release-7.noarch.rpm'
        ]

    def __list_packages(self):
        return [
            'bash-completion', 'yum-utils', 'sysstat', 'net-tools', 'gcc',
            'vim', 'git', 'openssl', 'openssl-devel', 'htop', 'wget'
        ]
