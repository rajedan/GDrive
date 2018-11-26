# GDrive
Mount your Google Drive in your Linux System.
--------------------------------------------------

* Introduction
* Requirements
* Installation/Setup
* Working Feature
* Future Scope
* Troubleshooting
* Authors

## Introduction
This is Linux File System Academic Project for mounting Google Drive as a Local Drive.
This project is based on FUSE library and google drive. Once google drive is mounted as local drive, 
you would be able to perform couple of operations like show, create, delete, edit files/directories 
and it will reflect into your google drive and vice versa as well.

## Requirements

1. Google account with access to google drive.
2. Linux machine(Note : We have tested it in Ubuntu 18.04.01 LTS)
3. python                   3.x.x
4. google-api-python-client	1.7.4 or above
5. google-auth	            1.6.1 or above
6. google-auth-httplib2	    0.0.3 or above
7. fusepy                   3.0.1 or above

## Installation/Setup

1. Google account : Register to [gmail](https://www.google.com/gmail/) account, if you do not have any google account. Now, you access your google drive and 
create some files and directory so that you could see these in mounted drive/directory.

2. Linux machine : This application is tested in Ubuntu 18.04.01 LTS. We expect this application to run in any Linux machines.

3. python 3.x.x : Install python 3 or any above version.
```bash
sudo apt-get install python3.6
```

4. google-api-python-client	:
```bash
pip install --upgrade google-api-python-client
```
5. google-auth :
```bash
pip install --upgrade oauth2client
```

6. google-auth-httplib2 :
```bash
pip install --upgrade httplib2
```

7. fusepy :
```bash
pip install fusepy
```
Refer [here](https://pypi.org/project/fusepy/) for installation reference and troubleshoot.

## Working Feature
> TODO
## Future Scope
> TODO
## Troubleshooting
> TODo
## Authors

* [Rajesh Dansena](https://github.com/rajedan) : 20163005
* [Svl Sarat Chandra](https://github.com/saratIIIT) : 2018202013
* [Yaswanth Koravi](https://github.com/yaswanthkoravi) : 2018202011
