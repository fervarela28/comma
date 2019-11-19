from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import requests
from datetime import datetime
# import urllib3.parse as urlparse
# from urllib3.parse import parse_qs


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/spreadsheets']

def email_parser(email):
    """Returns link of form 'http://newsletter...'
    Args:
        email (string): newsletter email with reservation.
    """
    availability_text = email.find('CHECK AVAILABILITY')
    print(email[availability_text:])
    first_link = email[:availability_text].rfind('http://newsletter')
    end_link = email[first_link:].find('\"') + first_link
    return email[first_link:end_link]

def find_corresponding_request(reservation_details, reservation_requests):
    venue_id = reservation_details['venue_id'][0]
    num_seats = reservation_details['num_seats'][0]
    time_slot = datetime.strptime(reservation_details['time_slot'][0], '%H:%M:%S')
    date = datetime.strptime(reservation_details['day'][0], '%Y-%m-%d')

    for res_request in reservation_requests[1:]:
        start_date = datetime.strptime(res_request[4], '%m/%d/%Y')
        end_date = datetime.strptime(res_request[5], '%m/%d/%Y')
        start_time = datetime.strptime(res_request[6], '%I:%M %p')
        end_time = datetime.strptime(res_request[7], '%I:%M %p')
        if(res_request[2] == venue_id and res_request[3] == num_seats and start_date <= date and end_date >= date):
            print('here')
        if (res_request[2] == venue_id and res_request[3] == num_seats and start_date <= date and end_date >= date and start_time <= time_slot and end_time >= time_slot):
            return res_request
    return 'No request found'

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    spreadsheetId = "191lNxeDXYXGvcxLsRYu194VcvDHqBnPJRwi4oxSEjdg"
    # values = [['d']]
    # body = {'values': values}
    # result = service.spreadsheets().values().update(
    #     spreadsheetId=spreadsheet_id, range=range_name,
    #     valueInputOption="USER_ENTERED", body=body).execute()
    service = build('gmail', 'v1', credentials=creds)
    service_sheets = build('sheets', 'v4', credentials=creds)
    #requests = service_sheets.spreadsheets().values().get(spreadsheetId="191lNxeDXYXGvcxLsRYu194VcvDHqBnPJRwi4oxSEjdg", range="A1:Z100").execute()['values']
    # Call the Gmail API
    results = service.users().messages().list(userId='me').execute()
    mes = service.users().messages().get(userId='me', id=results.get('messages')[0]['id']).execute()
    parts = mes['payload']
    email_info = parts['body']['data'].replace("-", "+").replace("_", "/")
    decoded = str(base64.b64decode(email_info))
    #print(decoded)
    newsletter = email_parser(decoded)
    print(newsletter)
    r = requests.get(url=newsletter)
    reservation_url = r.url
    print(reservation_url)
    # parsed = urlparse.urlparse(reservation_url)
    # reservation_details = urlparse.parse_qs(parsed.query)
    reservation_details = {'time_slot': ['22:30:00'], 'request_start': ['2019-12-17T17:00:00'], 'venue_id': ['1505'], 'request_end': ['2019-12-17T23:59:59'], 'num_seats': ['2'], 'day': ['2019-12-17']}
    print("Reservation details: ", reservation_details)
    reservation_requests = service_sheets.spreadsheets().values().get(spreadsheetId="191lNxeDXYXGvcxLsRYu194VcvDHqBnPJRwi4oxSEjdg", range="A1:Z100").execute()['values']
    print(find_corresponding_request(reservation_details, reservation_requests))
    labels = results.get('labels', [])

    if not labels:
        print('No labels found.')
    else:
        print('Labels:')
        for label in labels:
            print(label['name'])

if __name__ == '__main__':
    main()