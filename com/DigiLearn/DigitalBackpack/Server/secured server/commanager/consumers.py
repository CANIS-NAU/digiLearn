import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncJsonWebsocketConsumer
#from clientqueue.tasks import add
#from clientqueue.tasks import GDGetFileList
#from celery.result import AsyncResult
from GDriveInterfacetest import GetDriveList
from GDriveInterfacetest import DownloadFile

class ComConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'qwerty'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        #get gdrive files
        drivelist = GetDriveList()

        await self.accept()

        # begin creating JSON object to pass to client
        filedata = "{ "

        #iterate through each dictionary
        for d in drivelist:
            keylist = d.keys()
            if d.get("name") != None:

                # add the filename as key
                filedata =  filedata + "\"" + str(d.get("name")) + "\""

                # separate key/value pairs with a colon
                filedata = filedata + ":"

                # add the fileid as the value
                filedata = filedata + "\"" + str(d.get("driveID")) + "\""

                # dont print a coma after the last element
                if d != drivelist[-1]:
                    filedata = filedata + ", "

        filedata = filedata + " }"

        # send the filedata to the client
        await self.send(text_data=json.dumps({
            'raw': str(drivelist),
            'filedata': str(filedata)
        }))

    async def disconnect(self, close_code):
        # Leave room group
        # get disconnect time?
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        #get the file id
        fileid = text_data_json['fileid']

        DownloadFile(fileid)

        '''
        if (text_data_json['interpreter'] == 'GDrive'):
            message = 'Request sent to Google Drive: ' + text_data_json['message']
        elif (text_data_json['interpreter'] == 'GClass'):
            message = 'Request sent to Google Class: ' + text_data_json['message']
        elif (text_data_json['interpreter'] == 'GSearch'):
            message = 'Request sent to Google Search: ' + text_data_json['message']
        #TODO change this error message probably
        else:
            message = 'something went wrong' 

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
        '''

    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))

'''
#check routing.py for chatconsumer names
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'qwerty'
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )


        #get gdrive files
        drivelist = GetDriveList()

        filenames = ""

        for d in drivelist:
            keylist = d.keys()
            filenames =  filenames + str(d.get("name")) + "\n"

        await self.accept()

        await self.send(text_data=json.dumps({
            'message': str(filenames)
        }))

        

    async def disconnect(self, close_code):
        # Leave room group
        # get disconnect time?
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        add.delay(4,4)
        text_data_json = json.loads(text_data)

        if (text_data_json['interpreter'] == 'GDrive'):
            message = 'Request sent to Google Drive: ' + text_data_json['message']
        elif (text_data_json['interpreter'] == 'GClass'):
            message = 'Request sent to Google Class: ' + text_data_json['message']
        elif (text_data_json['interpreter'] == 'GSearch'):
            message = 'Request sent to Google Search: ' + text_data_json['message']
        #TODO change this error message probably
        else:
            message = 'something went wrong' 

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    async def chat_message(self, event):

        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
'''