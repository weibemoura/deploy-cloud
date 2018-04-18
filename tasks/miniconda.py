import os

from fabric.api import cd, run
from fabric.contrib import files
from fabric.operations import get, put

from core import content_file, create_tempfile
from core.base import BasicTask


class InstallMiniconda(BasicTask):

    def __init__(self):
        super(InstallMiniconda, self).__init__()

    def install(self):
        conda = 'Miniconda3-latest-Linux-x86_64'
        if not files.exists('/var/lib/miniconda'):
            run('yum install -y bzip2')
            with cd('/tmp'):
                run(f'wget https://repo.continuum.io/miniconda/{conda}.sh')
                run(f'chmod +x Miniconda3-latest-Linux-x86_64.sh && \
./Miniconda3-latest-Linux-x86_64.sh -b -p /var/lib/miniconda')

    def configure(self):
        if not files.contains('/etc/profile', 'miniconda'):
            put(self.__get_profile(), '/etc/profile')

        os.remove('./config/profile')
        run('source /etc/profile && conda update -n base conda -y')

    def __get_profile(self):
        get('/etc/profile', './config/profile')

        content = content_file('./config/profile')
        idx = content.index('export PATH')
        if idx > 0:
            content = content[:idx]
            content += 'PATH=$PATH:/var/lib/miniconda/bin\n'
            content += content[idx:]

        return create_tempfile(content)
