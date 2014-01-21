import os
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse,StreamingHttpResponse

# oauth2/google api imports
import httplib2
from apiclient.discovery import build
from oauth2client.django_orm import Storage
from oauth2.models import Oauth
from oauth2client.client import flow_from_clientsecrets
from oauth2client import gce
from oauth2client import xsrfutil
from apiclient import errors
from timesheet_site_v2 import settings

# CLIENT_SECRETS = os.path.join(os.path.dirname(__file__), 'client_secret.json')

# FLOW = flow_from_clientsecrets(
#     CLIENT_SECRETS,
#     # the auth url for the api
#     scope='https://www.googleapis.com/auth/drive',
#     # the url to call back to
#     redirect_uri='http://127.0.0.1:8000/oauth2/oauth2callback')

# Create your views here.
def index(request):

	# # get storage
	# storage = Storage(Oauth,'user',request.user,'credential')
	# # get the credentials from storage
	# credential = storage.get()
	# # if no credentials or if it doesnt exist
	# if credential is None or credential.invalid == True:
	# 	FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY,
	# 	                                                 request.user)
	# 	authorize_url = FLOW.step1_get_authorize_url()
	# 	return HttpResponseRedirect(authorize_url)
	# else:
	# 	# else use build() with credentials to access api
	# 	http = httplib2.Http()
	# 	http = credential.authorize(http)

	# api section

	# # google drive
	# service = build(serviceName='drive', version='v2', http=http)
	# all_files = retrieve_all_files(service)
	# return HttpResponse(str(all_files))

	return HttpResponse('OAuth 2.0')

def callback(request):
	# if not xsrfutil.validate_token(settings.SECRET_KEY, request.REQUEST['state'],
	#                                request.user):
	#   return  HttpResponseBadRequest()
	# credential = FLOW.step2_exchange(request.REQUEST)

	# storage = Storage(Oauth,'user',request.user,'credential')
	# storage.put(credential)

	return HttpResponseRedirect('/oauth2/')


# # for google drive
# def retrieve_all_files(service):

# 	result = []
# 	page_token = None
# 	while True:
# 		try:
# 			param = {}
# 			if page_token:
# 				param['pageToken'] = page_token
# 			files = service.files().list(**param).execute()

# 			result.extend(files['items'])
# 			page_token = files.get('nextPageToken')
# 			if not page_token:
# 				break
# 		except errors.HttpError, error:
# 			print 'An error occurred: %s' % error
# 			break
# 	return result