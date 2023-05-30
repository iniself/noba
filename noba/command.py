#!/usr/bin/env python

import os, sys, argparse
from noba.version import __version__
from pathlib import Path
from noba.snippet import load_json_file_if_not_exist_return_empty_dict, write_config_to_json_file, copyfile

try:
    package_absolute_path = Path(__file__).absolute().parent
    project_absolute_path = Path.cwd()

    sys.path.append(str(project_absolute_path))
except:
    pass

noba_template = package_absolute_path.joinpath('templates')

def canyou():
    if os.access('.', os.W_OK) and os.access('.', os.R_OK) and os.access('.', os.X_OK):
        return True
    return False

def main(**kwargs):
    if not canyou():
        raise Exception('You can not access the current folder. Try sudo maybe...')

    parser = argparse.ArgumentParser(
        prog='Noba',
        usage='%(prog)s [OPTION]',
        description='%(prog)s is not only backtrader',
        add_help=True,
    )

    parser.add_argument('-V', '--version', help='show %(prog)s version',  action='store_true')
    parser.add_argument('init', help='init your %(prog)s project',  nargs='?')
    parser.add_argument('more_config', help='generate more config file',  nargs='?')

    args = parser.parse_args()

    if args.version:
        print(f"noba version is: {__version__}")

    if args.init and args.init=='more_config':
        if not project_absolute_path.joinpath('config').exists():
            raise FileNotFoundError('must execute "noba init" first')        
        try:
            copy_template('config/project_config.json', 'config/project_config.json')        
        except Exception:
            raise IOError('Copying config template files failed. You can manually create them: config/project_config.json')
        
    if args.init and args.init=='init':
        try:
            make_project_dir()
        except Exception:
            raise IOError('There was an error creating the folder. Please check your execution permissions. Alternatively, you can creating by manually: bootstrap | migrate | pipeline | config | provider')

        try:
            copy_template('config/core_config.json', 'config/core_config.json')
        except Exception:
            raise IOError('Copying config template files failed. You can manually create them: config/core_config.json')

        try:
            copy_template('bootstrap/__init__.py', 'bootstrap/__init__.py')
            copy_template('bootstrap/boot_providers.py', 'bootstrap/boot_providers.py')
            copy_template('bootstrap/register_alias.py', 'bootstrap/register_alias.py')
            copy_template('bootstrap/register_providers.py', 'bootstrap/register_providers.py')
            copy_template('bootstrap/main.py', 'main.py')
        except Exception:
            print('Copying boot template files failed. You can manually create them')

        core_config = read_template('config/core_config.json')

        print(f'Let\'s init {parser.prog} project...', end="\n\n")

        connector = input("connector(mysql/sqLite/postgresql/...) :  ").lower() or 'mysql'
        host = input("host(localhost/...) :  ").lower() or 'localhost'
        port = input("port(3306/...) :  ") or '3306'
        database = input("database :  ")
        username = input("username :  ")
        password = input("password :  ")
        format = input("format(dataframe/list) :  ") or 'dataframe'
        core_config['db']['connector'] = connector
        core_config['db']['host'] = host
        core_config['db']['port'] = port
        core_config['db']['database'] = database
        core_config['db']['username'] = username
        core_config['db']['password'] = password
        core_config['db']['format'] = format

        try:
            write_config('config/core_config.json', core_config)
        except Exception:
            print('write config to json failed. You can manually edit json file under config folder')

def make_project_dir():
    if not check_dir_exist('bootstrap'):
        os.mkdir('bootstrap')

    if not check_dir_exist('migrate'):
        os.mkdir('migrate')

    if not check_dir_exist('pipeline'):
        os.mkdir('pipeline')

    if not check_dir_exist('config'):
        os.mkdir('config')

    if not check_dir_exist('services'):
        os.mkdir('services')

    if not check_dir_exist('provider'):
        os.mkdir('provider')

def copy_template(src, dst):
    dst_absolute_path = project_absolute_path.joinpath(dst)
    if not check_file_exist(dst_absolute_path):
        copyfile(noba_template.joinpath(src), dst_absolute_path)

def read_template(file_name):
    return load_json_file_if_not_exist_return_empty_dict(noba_template.joinpath(file_name))

def write_config(file_name, json):
    write_config_to_json_file(project_absolute_path.joinpath(file_name), json)

def check_dir_exist(dir):
    path = Path(dir)
    return path.exists() and path.is_dir()

def check_file_exist(file):
    file = Path(file)
    return file.exists() and file.is_file()

if __name__ == '__main__':
    main()
