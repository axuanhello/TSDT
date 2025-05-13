from fabric import task
from invoke import run as local
import os
import random

REPO_URL = 'https://github.com/axuanhello/TSDT.git'

@task
def deploy(c):
    site_folder = f'/home/{c.user}/sites/{c.host}'
    source_folder = site_folder+ '/source'

    _create_directory_structure_if_necessary(c, site_folder)
    _get_latest_source(c, source_folder)
    _update_settings(c, source_folder, c.host)
    _update_virtualenv(c, source_folder)
    _update_static_files(c, source_folder)
    _update_database(c, source_folder)

def _create_directory_structure_if_necessary(c, site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        c.run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(c, source_folder):
    if _exists(c,f'{source_folder}/.git'):
        c.run(f'cd {source_folder} && git fetch')
    else:
        c.run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', hide=True).stdout.strip()
    c.run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(c, source_folder, site_name):
    settings_path = source_folder+ '/notes/settings.py'
    secret_key_file = source_folder+ '/notes/secret_key.py'

    # 替代 DEBUG 和 ALLOWED_HOSTS 
    c.run(f"sed -i 's/DEBUG=True/DEBUG=False/' {settings_path}")
    c.run(f"sed -i 's/ALLOWED_HOSTS=.*/ALLOWED_HOSTS=[\"{site_name}\"]/' {settings_path}")

    if not _exists(c, secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-='
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        c.run(f'echo \'SECRET_KEY="{key}"\' > {secret_key_file}')

    # import secret_key 
    c.run(f'echo "" >> {settings_path}')
    c.run(f'echo "from .secret_key import SECRET_KEY" >> {settings_path}')

def _update_virtualenv(c, source_folder):
    virtualenv_folder = source_folder+ '/../virtualenv'
    pip_path = virtualenv_folder+ '/bin/pip'
    #python_path = virtualenv_folder+'/bin/python'

    if not _exists(c, pip_path):
        c.run(f'python3 -m venv {virtualenv_folder}')
    c.run(f'{pip_path} install -r {source_folder}/requirements.txt')

def _update_static_files(c, source_folder):
    c.run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database(c, source_folder):
    c.run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')

def _exists(c, path):
    
    result = c.run(f'test -e {path}', warn=True, hide=True)
    return result.ok
