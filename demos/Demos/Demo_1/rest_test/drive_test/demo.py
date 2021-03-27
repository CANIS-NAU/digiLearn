#local libraries
import os
import io
#google libraries kinda
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload

CLIENT_SECRET_FILE = 'client_secret.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

file_ids = ['1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq', '1PFhFIB25D9StfQU4qnuOh6kPdH9mchaS']
file_names = ['techFeasDoc.docx', 'paintAch.png']

for file_id, file_name in zip(file_ids,file_names):
    request = service.files().get_media(fileId = file_id)

    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fd = fh, request=request)

    done = False

    while not done:
        status, done = downloader.next_chunk()
        print('download progres {0}'.format(status.progress() * 100))

    fh.seek(0)

    with open(os.path.join('./files', file_name), 'wb') as f:
        f.write(fh.read())
        f.close()
