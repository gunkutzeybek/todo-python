import random
from fabric.contrib.files import append, exists
from fabric.api import cd, env, local, run, sudo
from fabric.network import ssh
from fabric.context_managers import prefix

REPO_URL = 'https://github.com/gunkutzeybek/todo-python.git'

ssh.util.log_to_file("paramiko.log", 10)

def deploy():    
    site_folder = f'/home/gunkut/sites/{env.host}'
    sudo(f'mkdir -p {site_folder}', user = 'gunkut')
    with cd(site_folder):
        _get_latest_source()
        _update_virtualenv()
        _create_or_update_dotenv()
        _update_static_files()
        _update_database()

def _get_latest_source():
    if exists('.git'):
        sudo('git fetch', user = 'gunkut')
    else:
        sudo(f'git clone {REPO_URL} .', user = 'gunkut')

    current_commit = local('git log -n 1 --format=%H', capture=True)
    sudo(f'git reset --hard {current_commit}', user = 'gunkut')

def _update_virtualenv():
    if not exists('virtualenv/bin/pip'):
        sudo(f'python3.6 -m venv virtualenv', user = 'gunkut')
    
    sudo('./virtualenv/bin/pip install -r requirements.txt', user = 'gunkut')

def _create_or_update_dotenv():
    append('.env', 'DJANGO_DEBUG_FALSE=y', use_sudo = True)
    append('.env', f'SITENAME={env.host}', use_sudo = True)
    current_contents = sudo('cat .env', user = 'gunkut')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(random.SystemRandom().choices(
            'abcdefghijklmnoprstuvwxyz0123456789', k=50
        ))
        append('.env', f'DJANGO_SECKRET_KEY={new_secret}', use_sudo = True)

def _update_static_files():
    sudo('./virtualenv/bin/python manage.py collectstatic --noinput', user = 'gunkut')

def _update_database():
    sudo('./virtualenv/bin/python manage.py migrate --noinput', user = 'gunkut')
    
