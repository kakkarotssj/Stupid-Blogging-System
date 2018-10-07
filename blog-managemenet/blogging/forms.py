from django import forms





class UserRegisterForm(forms.Form):
	first_name = forms.CharField(label="First Name", max_length=20)
	last_name  = forms.CharField(label="Last Name" , max_length=20)
	email 	   = forms.EmailField(label="Email")
	username   = forms.CharField(label="Username", max_length=20)
	password1  = forms.CharField(widget=forms.PasswordInput)
	password2  = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")



class UserLoginForm(forms.Form):
	username = forms.CharField(label="Username", max_length=20)
	password = forms.CharField(widget=forms.PasswordInput, label="Password")
	

class EditFirstNameForm(forms.Form):
	new_first_name = forms.CharField(label="New First Name", max_length=20)
	confirm_first_name = forms.CharField(label="Confirm New First Name", max_length=20)


class EditLastNameForm(forms.Form):
	new_last_name = forms.CharField(label="New Last Name", max_length=20)
	confirm_last_name = forms.CharField(label="Confirm New Last Name", max_length=20)


class EditUsernameForm(forms.Form):
	new_username = forms.CharField(label="New Username", max_length=20)
	confirm_new_username = forms.CharField(label="Confirm New Username", max_length=20)

class EditEmailForm(forms.Form):
	new_email = forms.EmailField(label="New Email")
	confirm_new_email = forms.EmailField(label="Confirm New Email")


class EditPasswordForm(forms.Form):
	new_password = forms.CharField(widget=forms.PasswordInput)
	confirm_new_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")



class BlogForm(forms.Form):
	title = forms.CharField(label="Blog Title", max_length=30)
	content = forms.CharField(widget=forms.Textarea)