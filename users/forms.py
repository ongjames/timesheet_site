from django import forms
from users.models import UserProfile,PrivateMessage
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):

	username = forms.CharField(max_length=30)
	email = forms.EmailField(max_length=30,required=True)
	password = forms.CharField(widget=forms.PasswordInput(),max_length=30)
	retype_password = forms.CharField(widget=forms.PasswordInput(),max_length=30,required=True)

	# clean and clean_* : validators

	# check if username has been taken
	def clean_username(self):
		username_data = self.cleaned_data.get('username')
		if User.objects.filter(username=username_data).count():
			self._errors["username"] = self.error_class(['Username has already been taken'])
		return username_data

	# check if email has already registered
	def clean_email(self):
		email_data = self.cleaned_data.get('email')
		if User.objects.filter(email=email_data).count():
			self._errors["email"] = self.error_class(['Email has already been registered'])
		return email_data

	# misc validators
	def clean(self):
		form_data = self.cleaned_data

		# matching passwords
		if form_data.get('password') != form_data.get('retype_password'):
			self._errors["retype_password"] = self.error_class(['Passwords must match'])
			self._errors["password"] = self.error_class(['Passwords must match'])
		return form_data

	class Meta:
		# use the User model
		model = User 
		# include only these fields
		fields = ('username', 'email', 'password')

class UserProfileForm(forms.ModelForm):
	comments = forms.CharField(required=False)
	comments.widget = forms.Textarea(attrs={'title':'Optional','rows':3})
	class Meta:
		model = UserProfile
		fields = ('comments',)


class PrivateMessageForm(forms.ModelForm):

	message = forms.CharField(required=False)
	message.widget = forms.Textarea(attrs={'rows':3})

	class Meta:
		model = PrivateMessage
		fields = ('message','to_user')

     