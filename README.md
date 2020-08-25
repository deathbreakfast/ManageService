# ManageService

A Python service that will check GitHub master branch for a repo. Anytime there is a new commit hash it will download all the files in the repo. It can also be configured to run a pre and post scripts when the files are deleted. 

Uses an `.ini` file to store the configuration.

## Requirements

* Python 3

## How to use
Durring the first run you will be propted for your Github user name and password. Followed by the repo and a pre and post script.

You can run using python 3.

`python3 manage-service.py`


## Installing from repo

`python3 setup.py install`

## Building binary

`python3 setup_cx.py build`


## TODO

* Migrate to use login token vs username password.
* Build service so it doesn't rely on python.
* Make a cask.
