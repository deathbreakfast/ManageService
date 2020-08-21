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

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    if 'login' not in config:
        username = input("Enter username: ")
        password = getpass()
        config['login'] = {'user': username,
                            'password': password}
        save_file(config)

    if "github" not in config:
        repo_url = input("Enter repopository. e.g. <user>/<repo_name>: ")
        config["github"] = {"repo": repo_url}
        save_file(config)

    if "actions" not in config:
        pre_update = input("Command to run if an update is avalible before files are downloaded: ")
        post_update = input("Command to run if an update is avalible after files are downloaded: ")
        config["actions"] = {"pre_update": pre_update, "post_update": post_update}
        save_file(config)

    # using username and password
    login = config["login"]
    g = Github(login["user"], login["password"])

    repo = g.get_repo(config["github"]["repo"])
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
        os.system(config["actions"]["pre_update"])
        contents = repo.get_contents("")
        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                if not os.path.isdir(file_content.path):
                    os.mkdir(file_content.path)
                contents.extend(repo.get_contents(file_content.path))
            else:
                # Create file
                with open(file_content.path, 'wb') as f:
                    f.write(file_content.decoded_content)

        os.system(config["actions"]["post_update"])



