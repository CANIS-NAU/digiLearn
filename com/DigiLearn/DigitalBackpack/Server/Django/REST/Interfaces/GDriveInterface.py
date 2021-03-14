import datetime
import pickle
import os
from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials




def create_service(user_auth, api_name, api_version, *scopes, user_email):
    _scopes = [scope for scope in scopes[0]]

    cred = None

    pickle_file = f'token_{api_name}_{api_version}.pickle'

    # gonna have to talk to sebo about the auth stuff here...
    # this might get moved to the authentication manager, again, talk to sebo about it
    
    if os.path.exists('credentials.json'):
        cred = Credentials.from_authorized_user_file('credentials.json', _scopes)
        print(cred)


    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            # this might not work because in the demo user_auth is a json file, not just a dict...
            flow = InstalledAppFlow.from_client_secrets_file(user_auth, _scopes)  # InstalledAppFlow.from_client_secrets_file(user_auth, _scopes)
            cred = flow.run_local_server()

        with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(api_name, api_version, credentials=cred)
        return service
    # this needs to be an actual exception, not a "catch all here"
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None


def convert_to_RFC_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt
