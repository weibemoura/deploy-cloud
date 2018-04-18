from hashlib import md5

from decouple import config
from fabric.api import run
from fabric.contrib import files
from fabric.operations import put

from core import content_file, create_tempfile
from core.base import BasicTask

pg_bin = config('PG_BIN')
pg_data = config('PG_DATA')
pg_password = config('PG_PASSWORD')


class InstallPgBouncer(BasicTask):

    def __init__(self):
        super(InstallPgBouncer, self).__init__()

        link = self.__link_repositories()
        run(f'yum install -y {link}', warn_only=True)

    def install(self):
        if not files.exists('/etc/pgbouncer/'):
            run('yum install -y pgbouncer')
            run('systemctl enable pgbouncer')

    def configure(self):
        if files.exists(f'{pg_data}/base'):
            run(f'PATH=$PATH:{pg_bin} PGPASSWORD={pg_password} psql -U postgres \
-c \"CREATE ROLE pgbouncer WITH LOGIN ENCRYPTED PASSWORD \'pgbouncer\';"',
                quiet=True)
            run(f'PATH=$PATH:{pg_bin} PGPASSWORD={pg_password} createdb -U \
postgres pgbench',
                quiet=True)

        put(self.__get_users(), '/etc/pgbouncer/userlist.txt')
        put(self.__get_pgbouncer(), '/etc/pgbouncer/pgbouncer.ini')
        run('systemctl restart pgbouncer')

    def __link_repositories(self):
        return 'https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/\
pgdg-centos10-10-2.noarch.rpm'

    def __get_users(self):
        content = ""
        users = (
            ('pgbouncer', 'pgbouncer'),
            ('production', 'production'),
            ('test', 'test'),
        )
        for user, password in users:
            hash_md5 = ''.join([password, user])
            hash_md5 = md5(hash_md5.encode()).hexdigest()
            hash_md5 = f'"{user}" "md5{hash_md5}" ""\n'
            content += hash_md5
        return create_tempfile(content)

    def __get_pgbouncer(self):
        content = content_file('./config/pgbouncer/pgbouncer.ini')
        content = content.replace('@@PASSWORD@@', pg_password)
        return create_tempfile(content)
