from __future__ import print_function
import requests
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

URL = "https://clist.by/api/v1/contest/"

# cc websites

PARAMS = {
	"username"       : "arpit_malhotra",
	"api_key"        : "43ba32f0766d96a69cf160b2c5b7be844b3e2931",
	"resource__name" : None,
	"start__gt"      : datetime.datetime.now().isoformat(timespec='minutes'),
	"duration__lt"   : 86400
}

TIMEZONE = "UTC"

def CreateEvents(contests):
	"""Shows basic usage of the Google Calendar API.
	Prints the start and name of the next 10 events on the user's calendar.
	"""
	print(contests)
	creds = None
	# The file token.pickle stores the user's access and refresh tokens, and is
	# created automatically when the authorization flow completes for the first
	# time.
	if os.path.exists('token.pickle'):
	    with open('token.pickle', 'rb') as token:
	        creds = pickle.load(token)
	# If there are no (valid) credsedentials available, let the user log in.
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

	service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
	for contest in contests:
		
		description = """URL: <a href=\"%s\">%s</a>""" % (contest["href"], contest["event"])

		event = {
			"summary": contest["event"],
			"description": description,
			"start": {
				"dateTime": contest["start"],
				"timeZone": TIMEZONE,
			},
			"end": {
				"dateTime": contest["end"],
				"timeZone": TIMEZONE,
			},
		
		}

		event = service.events().insert(calendarId='primary', body=event).execute()
		print("Event created: %s" % (event.get('htmlLink')))

def CallClist(resources):
	for resource in resources:
		PARAMS["resource__name"] = resource
		print(PARAMS)
		res = requests.get(url = URL, params = PARAMS)
		res = res.json()
		#print(res["objects"])
		CreateEvents(res["objects"])