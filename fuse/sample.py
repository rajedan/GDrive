from __future__ import print_function
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from apiclient.http import MediaFileUpload, MediaIoBaseDownload
import os,io

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v3', http=creds.authorize(Http()))

# for change detection
# print("before alteration: ")
# # while store is not None:
# response = service.changes().list(pageToken=1,
#                                                 spaces='drive').execute()
# for change in response.get('changes'):
#             # Process change
#     print('Change found for file: %s' % change.get('fileId'))

# if 'newStartPageToken' in response:
#             # Last page, save this token for the next polling interval
#     saved_start_page_token = response.get('newStartPageToken')
# page_token = response.get('nextPageToken')

def upload(filename,filepath):
    file_metadata = {'name': filename}
    media = MediaFileUpload(filepath)
    file = service.files().create(body=file_metadata,
                                    media_body=media,
                                    fields='id').execute()
    print('File ID: %s' % file.get('id'))
    return file.get('id')

def delete_file(file_name):
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for i in items:
            if i['name'] == file_name:
                service.files().delete(fileId=i['id']).execute()
                print("Deleted file with id:",i['id'])
                return
    return

def download(file_id,file_name):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))
    a=os.getcwd()+'/sam'
    with io.open(a+'/'+file_name,'wb') as f:
        fh.seek(0)
        f.write(fh.read())


def view():
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        # for i in items:
        #     print(i)
        pass
    return items
            
def all_upload():    
    a=os.getcwd()+'/sam'
    for i in os.listdir(a):
        upload(i,a+'/'+i)

def download_all():
    results = service.files().list(fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            download(item['id'],item['name'])

def create_folder(parent,name):
    if(parent==""):
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
    else:
        results = service.files().list(fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])
        for item in items:
            if(item['name']==parent):
                pid=item['id']
        file_metadata = {
            'name': name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents' : [pid]
        }

    file = service.files().create(body=file_metadata,
                                        fields='id').execute()
    print('Folder ID: %s' % file.get('id'))
    return


def meta():
    results = service.files().list(fields="nextPageToken, files(createdTime, modifiedTime, size )").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for i in items:
            print(u'{0}' u'{1}' u'{2}'.format(i['createdTime'],i['modifiedTime'],i['size']))
        
    

if __name__ == '__main__' :
    meta()
    