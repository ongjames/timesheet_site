from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from django.template import RequestContext

from users.models import UserProfile, PrivateMessage
from django.contrib import auth
from django.contrib.auth.models import User

from django.core.validators import validate_email

from users.forms import UserForm, UserProfileForm, PrivateMessageForm

from oauth2.models import Oauth

from datetime import datetime

def register(request):
    # init vars
    register_failure = []
    registered = False

    if request.method == 'POST':
        # get main user form
        user_form = UserForm(data=request.POST)
        # get user profile form
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            # save main user details
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # use the user details and save profile form
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            # use the user details and create oauth
            new_oauth = Oauth(user=user)
            new_oauth.save()

            # login the new user
            user_login = auth.authenticate(username=request.POST.get('username'),password=request.POST.get('password'))
            loggedin = auth.login(request, user_login) 
            if loggedin:
                registered = True

        else:
            print user_form.errors, profile_form.errors


    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
            'users/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def login(request):
    # init vars
    login_failure = []
    login_success = ''

    if not request.user.is_authenticated() and request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # login user
        user = auth.authenticate(username=username, password=password)

        if user :
            # user is active
            if user.is_active:
                auth.login(request, user)
                login_success = 'You have been successfully logged in'
            else:

                login_failure.append('Your account is disabled')
        else:


            login_failure.append('Invalid Login Details')


    return render(request,'users/login.html', {'login_failure':login_failure,'login_success':login_success})

def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/timesheet/')


def profile(request):
    # init vars
    email_errors = []
    password_cur_errors = []
    password_new_errors = []
    password_re_errors = []
    profile = ''

    if request.user.is_authenticated():

        profile = UserProfile.objects.get(user=request.user)

        if request.method == 'POST':

            # if the email field was used
            if request.POST.get('email'):
                try:
                    validate_email(request.POST.get('email'))
                    request.user.email = request.POST.get('email')
                    request.user.save()
                    return HttpResponseRedirect('/account/logout')
                except Exception, e:
                    email_errors.append('Not a valid email')
            # if any of the password fields were used
            elif request.POST.get('password_cur') or request.POST.get('password_new') or request.POST.get('password_re'):
                if not request.POST.get('password_cur'):    
                    password_cur_errors.append('You must enter your current password')
                else:
                    # check if password is valid
                    if not auth.authenticate(username=request.user.username, password=request.POST.get('password_cur')):
                        password_cur_errors.append('Your current password is invalid')
                if not request.POST.get('password_new'): 
                    password_new_errors.append('You must enter a new password')
                if request.POST.get('password_new') != request.POST.get('password_re'):
                    password_new_errors.append('Your new passwords must match')
                    password_re_errors.append('Your new passwords must match')
                # if there are no errors with the password fields
                if not password_cur_errors and not password_new_errors and not password_re_errors:
                    request.user.set_password(request.POST.get('password_new'))
                    request.user.save()
                    return HttpResponseRedirect('/account/logout')
            # if comments was changed
            elif request.POST.get('comments'):
                profile.comments = request.POST.get('comments')
                profile.user = request.user
                profile.save()
                return HttpResponseRedirect('/account/logout')

    return render(request,'users/profile.html',{'profile':profile, 'email_errors':email_errors,'password_cur_errors':password_cur_errors,'password_new_errors':password_new_errors,'password_re_errors':password_re_errors})

def pm(request):
    all_messages = []
    pm_form = []

    sent_message = ''
    if request.user.is_authenticated and request.user.is_active:

        all_messages = PrivateMessage.objects.filter(to_user=request.user).order_by('-message_time')
        if request.method == 'POST':
            pm_form = PrivateMessageForm(data=request.POST)
            pm_date = pm_form.save(commit=False)
            pm_date.message_time = datetime.now()
            pm_date.from_user = request.user
            pm_date.save()
            sent_message = 'Message sent to user '+pm_date.to_user.username
        else:
            pm_form = PrivateMessageForm()


    return render(request,'users/private_message.html',{'all_messages':all_messages,'pm_form':pm_form,'sent_message':sent_message})


def resetpw(request):
    reset_message = ''

    if request.method == 'POST' and not request.user.is_authenticated():

        try:
            valid_user = User.objects.get(email=request.POST.get('email'))
            new_pw = User.objects.make_random_password(length=8)
            # new_pw = 'TEST'
            valid_user.set_password(new_pw)
            valid_user.save()
            reset_message = 'Password changed successfully.  New password has been set to: "'+new_pw+'" (will have proper email and decaying password in the future)' 
        except Exception, e:
            reset_message = 'Email could not be found'

            

    return render(request,'users/resetpw.html',{'reset_message':reset_message})