from decouple import config
from fabric.api import run, settings
from fabric.contrib import files
from fabric.operations import put

from core import content_file, create_tempfile
from core.base import BasicTask

pg_bin = config('PG_BIN')
pg_data = config('PG_DATA')
pg_user = config('PG_USER')
pg_password = config('PG_PASSWORD')
pg_encoding = config('PG_ENCODING')
pg_locale = config('PG_LOCALE')


class InstallPostgreSQL(BasicTask):

    def __init__(self):
        super(InstallPostgreSQL, self).__init__()

        link = self.__link_repositories()
        run(f'yum install -y {link}', warn_only=True)

    def install(self):
        if not files.exists(pg_bin):
            packages = ' '.join(self.__list_packages())
            run(f'yum install -y {packages}')
            run(f'echo -e "{pg_password}\n{pg_password}" | passwd {pg_user}',
                quiet=True)
            run('systemctl enable postgresql-10')

    def configure(self):
        if not files.exists(f'{pg_data}/base'):
            with settings(user='postgres', password=pg_password):
                run(f'mkdir -p {pg_data}/../wals')
                run(f'PATH=$PATH:{pg_bin} initdb -D {pg_data} -U {pg_user} \
-E {pg_encoding} --locale={pg_locale}')

            put(self.__config_pg_hba('trust'), f'{pg_data}/pg_hba.conf')
            run('systemctl restart postgresql-10')

            with settings(user='postgres', password=pg_password):
                run(f'PATH=$PATH:{pg_bin} psql -U {pg_user} -c "ALTER USER {pg_user} \
WITH ENCRYPTED PASSWORD \'{pg_password}\';"',
                    quiet=True)

            put(self.__config_pg_hba('md5'), f'{pg_data}/pg_hba.conf')
            put(self.__config_postgresql(), f'{pg_data}/postgresql.conf')
            run('systemctl restart postgresql-10')

    def __link_repositories(self):
        return 'https://download.postgresql.org/pub/repos/yum/10/redhat/rhel-7-x86_64/\
pgdg-centos10-10-2.noarch.rpm'

    def __list_packages(self):
        return [
            'postgresql10', 'postgresql10-server', 'postgresql10-contrib',
            'postgresql10-devel'
        ]

    def __config_pg_hba(self, method):
        content = content_file('./config/postgresql/pg_hba.conf')
        content = content.replace('@@METHOD@@', method)
        return create_tempfile(content)

    def __config_postgresql(self):
        costom_config = f"""listen_addresses = '127.0.0.1'
port = 5432
max_connections = 200
wal_level = replica # ou hot_standby no postgresql < 10
wal_keep_segments = 100
max_wal_senders = 5
#archive_mode = on
#archive_command = 'cp "%p" "{pg_data}/../wals/%f"'

max_connections = 20
shared_buffers = 512MB
effective_cache_size = 1GB
work_mem = 12MB
maintenance_work_mem = 512MB
min_wal_size = 80MB
max_wal_size = 1GB
# (checkpoint_timeout - 2min) / checkpoint_timeout
checkpoint_completion_target = 0.7
checkpoint_timeout = 7min
wal_buffers = 16MB
default_statistics_target = 100
effective_io_concurrency = 200
max_worker_processes = 4
max_parallel_workers_per_gather = 2
max_parallel_workers = 4
random_page_cost = 1.1\n"""

        content = content_file('./config/postgresql/postgresql.conf')
        content = content.replace('@@CUSTOM_CONFIG@@', costom_config)
        return create_tempfile(content)
