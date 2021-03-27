from __future__ import absolute_import, unicode_literals
from REST.Interpreters import GDriveInterpreter #TODO: clean up pathing later

from celery import shared_task

@shared_task
def add(x, y):
    return x+y

@shared_task
def GDInterfaceTest():
    cred = 'credentials.json'
    fileid = '1SML1QNgHzt-iUPTjfmV__UzPdg7xGErq'

    meta = GDriveInterpreter.get_file_metadata(cred, fileid)

    print(meta)

@shared_task
def GDGetFileList():
    cred = 'credentials.json'
    fileid = '1ZBc6zCt0uPDl2YVC16E0aLWik1I5PzBWxgzO_XdhMDw'

    file_list = GDriveInterpreter.get_file_list(cred, "my-drive")

    print(file_list)

#TODO: GSearchRequest

#TODO: GDriveRequestFile

#TODO: GDriveSendFile

#TODO: GClassRequest

