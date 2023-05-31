import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def _get_credentials():
    cred_pickle_file = 'credentials.pickle'
    client_secrets_file = 'client_secret_27192482107-504i6hgku4b5gqiuppj4fk2uava2vln8.apps.googleusercontent.com.json'
    gsheets_api = 'https://www.googleapis.com/auth/spreadsheets'

    # Load credentials
    creds = None
    if os.path.exists(cred_pickle_file):
        with open(cred_pickle_file, 'rb') as f:
            creds = pickle.load(f)
    # If no valid credentials found, authenticate and authorize the script
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, [gsheets_api])
            creds = flow.run_local_server(port=0)
        # Save the credentials for future use
        with open(cred_pickle_file, 'wb') as f:
            pickle.dump(creds, f)

    return creds

def _create_service():
    # Create a service instance
    service = build('sheets', 'v4', credentials=creds)
    return service

def _create_sheet(spreadsheet_id='1SVS130kLYgIcoJmyXWJoXdm1Kv6DVkZJRjucaS95X8Q', sheet_name='R05CB', columns=[]):
    try:
        # Check if the sheet already exists
        existing_sheets = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute().get('sheets', [])
        sheet_exists = any(sheet['properties']['title'] == sheet_name for sheet in existing_sheets)

        if sheet_exists:
            print(f'Sheet "{sheet_name}" exists.')
        else:
            print(f'Sheet "{sheet_name}" doesn\'t exist. Creating...')
            # Create the new sheet
            request = {
                'addSheet': {
                    'properties': {
                        'title': sheet_name
                    }
                }
            }
            service.spreadsheets().batchUpdate(
                spreadsheetId=spreadsheet_id,
                body={'requests': [request]}
            ).execute()

            print(f'Sheet "{sheet_name}" created.')

        # Creating columns
        sheet_range = sheet_name + '!A1'
        body = {'values': [columns]}

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=sheet_range,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f'{result.get("updatedCells")} cells updated.')
        return True
    except Exception as e:
        print(e)
        return False

def _append_data(spreadsheet_id='1SVS130kLYgIcoJmyXWJoXdm1Kv6DVkZJRjucaS95X8Q', sheet_name='Connection Stats', row_data=[]):
    sheet_range = sheet_name + '!A2'
    body = {'values': [row_data]}

    result = service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range=sheet_range,
        valueInputOption='RAW',
        body=body
    ).execute()

    print(f'{result.get("updatedCells")} cells updated.')
    return True

creds = _get_credentials()
service = _create_service()

station_name='R05CB'
connection_sheet_name='Connection Stats'

columns = [
    'Set Station Name',
    'Latitude',
    'Longitude',
    'Elevation (m)',
    'Sending IP address',
    'Port',
    'Number of channels',
    'Transmission freq.',
    'Transmission rate',
    'Samples per second',
    'Inventory'
]

conn_stats = [
    'R24FA',
    '16.123',
    '16.123',
    '16.123',
    '192.168.0.4',
    '18069',
    '4',
    '250 ms/packet',
    '4 packets/sec',
    '100 sps',
    'AM.R24FA (Raspberry Shake Citizen Science Station)',
]
_create_sheet(sheet_name=connection_sheet_name, columns=columns)
_append_data(sheet_name=connection_sheet_name, row_data=conn_stats)

event_columns = [
    'event_time',
    'floor_num',
    'acc_x',
    'acc_y',
    'acc_z',
    'disp_units',
    'disp_x',
    'disp_thresh_x',
    'drift_x',
    'drift_thresh_x',
    'over_drift_thresh_x',
    'disp_y',
    'disp_thresh_y',
    'drift_y',
    'drift_thresh_y',
    'over_drift_thresh_y',
    'disp_z',
    'disp_thresh_z',
    'drift_z',
    'drift_thresh_z',
    'over_drift_thresh_z',
    'axis_with_max_drift'
]


event_data = [
    '2023-05-18T14:03:20.12Z',
    '8',
    '0.01478191698324985',
    '5423.077433066255',
    '5421.818985401211',
    'centimeters',
    '0.003161',
    '40.03786417307067',
    '40.029502518385996',
    '003161',
    '003161',
    '1.478192',
    '003161',
    '003161',
    '003161',
    '003161',
    '003161.786417',
    '786417',
    '003161',
    '003161',
    '003161',
    'x'
]

_create_sheet(sheet_name=station_name, columns=event_columns)
_append_data(sheet_name=station_name, row_data=event_data)
