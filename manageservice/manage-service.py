import argparse
import os

from getpass import getpass

import configparser
from github import Github


CONFIG_FILE_NAME = 'manage-service.ini'

def save_file(config):
    with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

def set_and_save_sha(config):
    config["github"]["current_commit"] = branch.commit.sha
    save_file(config)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script to check a Github repo, pull contents and run'
            + "pre and post flight commands.\n All arguments are required on first run.\nSubsequent runs"
            + 'will attempt to load them from the config. Provide them again to override')
    parser.add_argument('--repo', help='Github repository. e.g. <user>/<repo_name>')
    parser.add_argument('--user', help='Github username')
    parser.add_argument('--pwd', help='Github password')
    parser.add_argument('--dir', help='Directory to install to')
    parser.add_argument('--pre', help='Preflight script to run before downloading the files from Github')
    parser.add_argument('--post', help='Postflight script to run after downloading is complete')

    args = parser.parse_args()

    repo = args.repo
    user = args.user
    pwd = args.pwd
    dirl = args.dir
    pre = args.pre
    post = args.post


    config = configparser.RawConfigParser()
    config.read(CONFIG_FILE_NAME, encoding='utf-8')

    if not repo:
        if 'github' not in config:
            raise ValueError("Could not find an existing config and argument 'repo' was not provided. Check "                    + 'the help section for more details. -h')
        repo = config['github']['repo']
    else:
        config["github"] = {"repo": repo}
        save_file(config)

    if not user or not pwd:
        if 'login' not in config:
            raise ValueError('Could not find existing config and arguments for username or password missing. '
                    + 'Check the help section for more details. -h')
        user = config['login']['user']
        pwd = config['login']['password']
    else:
        config['login'] = {'user': user, 'password': pwd}
        save_file(config)

    if not dirl:
        if 'directory' not in config:
            raise ValueError('Could not find existing config and arguments for directory are missing. Check '
                    + 'the help section for more details. -h')
        dirl = config['directory']['dir']
        save_file(config)
    else:
        config['directory'] = {'dir': dirl} 
        save_file(config)

    if not pre or not post:
        if 'actions' not in config:
            raise ValueError('Could not find existing config and arguments for pre or post flight missing. '
                    + 'Check the help section for more details. -h')
        pre = config['actions']['pre_update']
        post = config['actions']['post_update']
    else:
        config["actions"] = {"pre_update": pre, "post_update": post}
        save_file(config)
    
    # using username and password
    g = Github(user, pwd)

    repo = g.get_repo(repo)
    branch = repo.get_branch("master")

    run_update = False

    if "current_commit" not in config["github"]:
        set_and_save_sha(config)
        run_update = True
    if config["github"]["current_commit"] != branch.commit.sha:
        set_and_save_sha(config)
        run_update = True

    run_update = True
    if run_update:
        os.system(pre)

        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop()
            full_path = os.path.join(dirl, file_content.path)

            if file_content.type == "dir":
                if not os.path.isdir(full_path):
                    os.mkdir(full_path)

                contents.extend(repo.get_contents(file_content.path))
            else:
                # Create file
                with open(full_path, 'wb') as f:
                    f.write(file_content.decoded_content)

        os.system(post)



