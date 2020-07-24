from django.shortcuts import render, HttpResponse , redirect
from django.views import View
from .zoho import tokenmanager, accesstokenmanager, profilemanager
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email,DecimalValidator
# Create your views here.

class home(View):
	"""main page view"""
	def get(self, request):
		return redirect("userlogin")

class zohoadmin(View):
	"""zoho auth login page view"""
	def get(self, request):
		if request.user.is_superuser:
			zoho = tokenmanager()
			status = tokenmanager.tokenstatus()
			return render(request,"zohotoken.html",context={"tokenlogin": zoho.tokenlogin(), "status" : status })
		else:
			return HttpResponse("Not found")

class mytoken(View):
	"""firt time token page view"""
	def get(self, request):
		accessm = accesstokenmanager()
		auth_code = request.GET['code']
		location = request.GET['location']
		accounts_server = request.GET['accounts-server']
		firsttimetoken = accessm.firsttimetoken(auth_code).json()
		token = tokenmanager.tokensave(tokendatas=firsttimetoken)
		return redirect("zohoadmin")
#=========================admin outh end First time ========================================
#=====================access token manage start ====================================

class register(View):
	"""register page view"""
	def get(self, request):
		form = SignUpForm()
		return render(request, "signup.html", {'form': form})
	def post(self, request):
		form = SignUpForm(request.POST)
		myform = SignUpForm(request.POST)
		if form.is_valid():
			response_code = accesstokenmanager().leadstore(form,request)
			user=form.save()
			user.refresh_from_db()
			user.profile.mob = form.cleaned_data.get('mob')
			user.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			try:
				next = request.GET['next']
			except:
				next="/profile"
				return redirect(next)
		else:
			return render(request, 'signup.html', {'form': form,'myform': myform})
class userlogin(View):
	""" Login page view"""
	def get(self,request):
		form = AuthenticationForm()
		return render(request, 'login.html', {'form': form})

	def post(self, request):
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			user = form.get_user()
			login(request, user)
			try:
				next = request.GET['next']
			except:
				next="/profile"
			return redirect(next)
		return redirect("userlogin")



def userlogout(request):
	"""logout page view"""
	logout(request)
	return render(request,"logout.html")

class profile(View):
	"""profile page view"""
	def get(self, request):
		pm = profilemanager()
		return render(request,"profile.html", context={"profile": pm.get_profile(request)})

class editprofile(View):
	"""profile edit page view"""
	def get(self, request):
		return render(request, "editprofile.html")
	def post(self, request):
		form = request.POST.dict()
		username = request.user.username
		user1 = User.objects.get(username=username)
		email = form['Email']
		phone = form['mob']
		if email:
			try:
				validate_email(email)
			except ValidationError as e:
				return redirect("editprofile")
			user1.email = email
		if phone:
			try:
				int(phone)
			except:
				return redirect("editprofile")
			user1.profile.mob = phone
		user1.save()
		return redirect("profile")
def errorpage(request):
	return HttpResponse('{"status" : "error", "connection " : "failed, "solution" : please connect the zoho crm " }')
def test(request):
	dp = accesstokenmanager()
	data = {
		"username" : "rajkumar",
		"email" : "xyz@gmail.com",
		"mobile_number" : "9876787656",
	}
	response = dp.leadupdate(data,request)

	return HttpResponse(response)