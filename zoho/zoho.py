from .models import tokenmanager as tm
from django.shortcuts import get_object_or_404
import requests
import json
from datetime import datetime
from django.utils import timezone
from datetime import timedelta  
class tokenmanager:
	def __init__(self):
		"""Assing client id client secret and redirect url"""
		self.client_id = "1000.25CT0LKAERAZKNEX469KMWTLZMLP0K"
		self.client_secret = "9b841797ec927a1a0b5bdae9e0789c31bda2ca4245"
		self.redirect_uri = "http://localhost:8000/mytoken"

	def client_id_get(self):
		"""create getter method for client id"""
		return self.client_id

	def client_secret_get(self):
		"""create getter method for client secret """
		return self.client_secret

	def redirect_uri_get(self):
		"""create getter method for redirect url"""
		return self.redirect_uri

	def tokenlogin(self):
		"""create a zoho crm api auth login url"""
		base_url = "https://accounts.zoho.com/oauth/v2/auth?scope=ZohoCRM.users.ALL,ZohoCRM.Modules.ALL&client_id={}&response_type=code&access_type=offline&prompt=consent&redirect_uri={}".format(self.client_id,self.redirect_uri)
		return base_url
	def tokensave(tokendatas):
			"""save the token into database"""
			gettokendata = tm.objects.filter(id=1)
			expire_time = int(tokendatas['expires_in'])
			expire_in = datetime.now() + timedelta(seconds=expire_time)

			if gettokendata:
				gettokendata.update(access_token = tokendatas['access_token'],refresh_token=tokendatas['refresh_token'], api_domain= tokendatas['api_domain'], token_type = tokendatas['token_type'] , expires_in=expire_in)
				return gettokendata
			else:
				tokendata = tm()
				tokendata.access_token = tokendatas['access_token']
				tokendata.refresh_token = tokendatas['refresh_token']
				tokendata.api_domain = tokendatas['api_domain']
				tokendata.token_type = tokendatas['token_type']
				tokendata.expires_in = expire_in
				tokendata.save()
				return tokendata
	def tokenstatus():
			"""auth is available or not in databasee"""
			gettokendata = tm.objects.all().count()
			if gettokendata>0:
				return True
			return False
class accesstokenmanager:
	def firsttimetoken(self,auth_code):
		"""use auth login first time to genrate token"""
		base_url = "{}/oauth/v2/token".format("https://accounts.zoho.in")
		tokenm = tokenmanager()
		client_id = tokenm.client_id
		client_secret = tokenm.client_secret
		redirect_uri = tokenm.redirect_uri
		code = auth_code
		grant_type = "authorization_code"
		body = {
			"grant_type" : grant_type,
			"client_id" : client_id,
			"client_secret" : client_secret,
			"redirect_uri" : redirect_uri,
			"code" : code,
		}
		response = requests.post(base_url, data=body)
		return response
	def refresh_token(self):
		""" use refresh token to create new valid tokens   """
		tokenm = tokenmanager()
		client_id = tokenm.client_id_get()
		client_secret = tokenm.client_secret_get()
		refresh_token = tm.objects.get().refresh_token
		base_url = "https://accounts.zoho.in/oauth/v2/token?refresh_token={}&client_id={}&client_secret={}&grant_type=refresh_token".format(refresh_token,client_id,client_secret)
		response = requests.post(base_url).json()
		access_token = response['access_token']
		expires_time = int(response['expires_in'])
		expire_in = datetime.now() + timedelta(seconds=expires_time)
		gettokendata = tm.objects.filter(id=1)
		gettokendata.update(access_token=access_token,expires_in=expire_in)
		#response_code = tokenm.tokensave(tokendatas= response)
		return response.items()
	def get_access_token(self,request):
		"""get access token """
		access_token_data = tm.objects.get()
		current_time = timezone.now()
		token_expire_time = access_token_data.expires_in
		if token_expire_time < current_time:
			self.refresh_token()
			access_token_data = tm.objects.get()
			request.session['access_token'] = access_token_data.access_token
			return access_token_data.access_token
		else:
			access_token_data = tm.objects.get()
			request.session['access_token'] = access_token_data.access_token
			return access_token_data.access_token
	def leadstore(self,form, request):
		"""prepare data  and store in dict"""
		username = form.cleaned_data.get('username')
		email = form.cleaned_data.get('email')
		mobile_number = form.cleaned_data.get('mob')
		data = {
			"username" : username,
			"email" : email,
			"mobile_number" : mobile_number,
		}
		response = self.leadinsert(data,request)
		return response

	def leadinsert(self,data, request):
		""" insert the data into zoho crm"""
		base_url = "https://www.zohoapis.in/crm/v2/Contacts"
		access_token = self.get_access_token(request)
		Zoho_oauthtoken = "Zoho-oauthtoken {}".format(access_token)
		header = {
			"Authorization" : Zoho_oauthtoken
		}
		bodydata ={
			"data" : [
				{
					"Last_Name" : data['username'],
					"Email" : data['email'],
					"Phone" : str(data['mobile_number']),
				}
					],
			"duplicate_check_fields": [
				"Last_Name"
			],
			"trigger": [
				"approval"
			]
		}
		response_code = requests.post(base_url,headers= header, data = json.dumps(bodydata))#.json()['data'][0]['status']

		return response_code


class profilemanager:
	""" get profile details"""
	def get_profile(self,request):
		mob = request.user.profile.mob
		email = request.user.email
		username = request.user.username
		data = {
			"mob": mob,
			"email" : email,
			"username" : username,
		}
		return data
		

