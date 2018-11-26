# GDrive

**Mount your Google Drive in your Linux System.**

## Getting Started
* Introduction
* Requirements
* Installation/Setup
* Configuration/How to Run
* Working Features
* Future Scope
* Troubleshooting
* Authors

### Introduction
This is Linux File System Academic Project for mounting Google Drive as a Local Drive.
This project is based on FUSE library and google drive. Once google drive is mounted as local drive, 
you would be able to perform couple of operations like show, create, delete, edit files/directories 
and it will reflect into your google drive and vice versa as well.

### Requirements

1. Google account with access to google drive.
2. Linux machine(Note : This application has been tested in Ubuntu 18.04.01 LTS)
3. python                   3.x.x
4. google-api-python-client	1.7.4 or above
5. google-auth	            1.6.1 or above
6. google-auth-httplib2	    0.0.3 or above
7. fusepy                   3.0.1 or above

### Installation/Setup

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
Refer [here](https://pypi.org/project/fusepy/) for fusepy installation reference and troubleshoot.

### Configuration/How to Run
>TODO : write about configuring secret.json
1. Clone the repository :
```bash
git clone git@github.com:rajedan/GDrive.git
```
or download and unzip it.

2. Create two empty directory. For example : ~/temp1 ~/temp2
Here, temp1 directory is where we are going to mount the google drive and 
temp2 directory will be used as temporary directory for different operations. 
Please do not store anything here.
3. Open Terminal and navigate to ```GDrive/fuse/``` and run the below command:
python myfuse.py ~/temp1 ~/temp2
4. For the first time, It will open browser and ask to login into your gmail account and 
ask for permission. This is one time setup and won't ask on next run. Please login and accept permission.
5. temp1 is the directory where google drive has been mounted. Now open temp1 directory in terminal/file explorer and you can perform the features mentioned.

### Working Features
1. ```ls``` and ```ls -lrt``` command in mounted directory. It will list out all the files and folders of google drive.

2. Create Folder through File explorer in mounted directory. New Folder will be reflected into google drive.

3. Delete Folder through File explorer in mounted directory. Folder deletion will be reflected into google drive.

4. Create or copy-paste a txt or image File through File explorer. New File will be reflected into google drive.

5. Edit any existing txt File through File explorer and gedit or through vi in terminal. Changes will be reflected into the file in google drive after saving the file changes.

6. Delete any file and file deletion will be reflected in google drive as well.

7. Create/Delete/Edit any file or folder in google drive and you can see the changes through ```ls``` or other commands in local mounted directory.

### Future Scope

There can be numerous scope to this project. Some of them are as follows:
* File/Folder access or deletion based on it's ownership.
* Access to Google drive Trash and moving files/folders to Trash on deletion instead of permanent delete. etc.

### Troubleshooting

* We have came across error when you exhaust the google drive API daily limit. In this case, you need to use different account for setup or wait and use next day.
* Please shoot a mail to authors or file a bug [here](https://github.com/rajedan/GDrive/issues) stating the scenarios and screenshots/logs (if any).

### Authors

* [Rajesh Dansena](https://github.com/rajedan) : 20163005
* [Svl Sarat Chandra](https://github.com/saratIIIT) : 2018202013
* [Yaswanth Koravi](https://github.com/yaswanthkoravi) : 2018202011


