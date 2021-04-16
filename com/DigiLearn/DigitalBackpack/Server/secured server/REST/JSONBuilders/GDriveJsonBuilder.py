import json

_none = type(None)

def createfilejson(fileobj):
    # assumes fileobj is DigiJsonBuilder.create_file()

    gdrivejson = {
        'name': fileobj['name']
    }

    return gdrivejson


def add_file_attachment(fileid):
    return {
            'addAttachments':[
                {
                    'driveFile': {
                        'id': fileid
                    }
                }
            ]
        }
