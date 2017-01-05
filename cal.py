from __future__ import print_function
import httplib2
import os
import time

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime
import pytz   
import tzlocal

try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
	"""Gets valid user credentials from storage.

	If nothing has been stored, or if the stored credentials are invalid,
	the OAuth2 flow is completed to obtain the new credentials.

	Returns:
		Credentials, the obtained credential.
	"""
	home_dir = os.path.expanduser('~')
	credential_dir = os.path.join(home_dir, '.credentials')
	if not os.path.exists(credential_dir):
		os.makedirs(credential_dir)
	credential_path = os.path.join(credential_dir,
								   'calendar-python-quickstart.json')

	store = Storage(credential_path)
	credentials = store.get()
	if not credentials or credentials.invalid:
		flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
		flow.user_agent = APPLICATION_NAME
		if flags:
			credentials = tools.run_flow(flow, store, flags)
		else: # Needed only for compatibility with Python 2.6
			credentials = tools.run(flow, store)
		print('Storing credentials to ' + credential_path)
	return credentials

def main():
	"""Shows basic usage of the Google Calendar API.

	Creates a Google Calendar API service object and outputs a list of the next
	10 events on the user's calendar.
	"""
	credentials = get_credentials()
	http = credentials.authorize(httplib2.Http())
	service = discovery.build('calendar', 'v3', http=http)

	now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
	print (now)
	print('Getting the upcoming 10 events')
	eventsResult = service.events().list(
		calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
		orderBy='startTime').execute()
	events = eventsResult.get('items', [])

	if not events:
		print('No upcoming events found.')
	for event in events:
		start = event['start'].get('dateTime', event['start'].get('date'))
		print(start, event['summary'])

		
class googlecal():
	def __init__(self):
		self.credentials = get_credentials()
		self.http = self.credentials.authorize(httplib2.Http())
		self.service = discovery.build('calendar', 'v3', http=self.http)
		
		self.termine = []
		self.stermine = []
	
	def nextevents(self):
		self.termine = []
		now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
		time_last = datetime.datetime.utcnow()+datetime.timedelta(hours=20)
		time_last = time_last.isoformat() + 'Z'
		calendarsResult = self.service.calendarList().list().execute()
		calendars = calendarsResult.get("items", [])
		for calendar in calendars:
			calname = calendar["summary"]
			#print (calname)
			calcolor = calendar["backgroundColor"]
			
			eventsResult = self.service.events().list(
				calendarId=calendar["id"], timeMin=now, timeMax=time_last, maxResults=3, singleEvents=True,
				orderBy='startTime', timeZone="UTC").execute()
			events = eventsResult.get('items', [])
			
			for event in events:
				start = event['start'].get('dateTime', event['start'].get('date'))
				try:
					start = self.utc2local(datetime.datetime.strptime(start,"%Y-%m-%dT%H:%M:%SZ")).timestamp()
					end = event['end'].get('dateTime', 0)
					end = self.utc2local(datetime.datetime.strptime(end,"%Y-%m-%dT%H:%M:%SZ")).timestamp()
				except:
					start = self.utc2local(datetime.datetime.strptime(start,"%Y-%m-%d")).timestamp()
					end = 0
				event_name =  event['summary']
				self.termine.append([calname, calcolor, start, end, event_name])

				
		#print (self.termine)
		self.stermine = sorted(self.termine, key=lambda a: a[2])
		return self.stermine
	
	def utc2local (self, utc):
		local_timezone = tzlocal.get_localzone() 
		return utc.replace(tzinfo=pytz.utc).astimezone(local_timezone)
	

if __name__ == '__main__':
	cal = googlecal()
	cal.nextevents()