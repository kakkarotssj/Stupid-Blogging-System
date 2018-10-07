# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from .forms import (UserLoginForm, UserRegisterForm, 
	EditFirstNameForm, EditLastNameForm, EditUsernameForm, EditEmailForm, EditPasswordForm,
	BlogForm)

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect

from django.core import exceptions

from django.contrib.auth.decorators import login_required

from .models import Profile, Blog

# Create your views here.


def home_view(request):
	context = {}
	template_name = "blogging/home.html"

	return render(request, template_name, context)



def login_view(request):
	context = {}
	template_name = "blogging/login.html"

	if request.user.is_authenticated():
		redirect_url = "/profile/" + str(request.user)
		return HttpResponseRedirect(redirect_url)

	login_form = UserLoginForm(request.POST or None)
	context['login_form'] = login_form
	if login_form.is_valid():
		username = login_form.cleaned_data.get("username")
		password = login_form.cleaned_data.get("password")

		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)

			redirect_url = "/profile/" + str(username)
			return HttpResponseRedirect(redirect_url)
		else:
			try:
				if_any_exists = User.objects.get(username=username)
				context["error"] = "Password is not right. Please try again."
			except exceptions.ObjectDoesNotExist:
				context["error"] = "This user does not exist. Please Try again."

			return render(request, template_name, context)



	return render(request, template_name, context)


def register_view(request):
	context = {}
	template_name = "blogging/register.html"

	register_form = UserRegisterForm(request.POST or None)
	context['register_form'] = register_form

	if register_form.is_valid():
		try:
			username = register_form.cleaned_data.get('username')

			if_any_exists = User.objects.get(username=username)

			context["error"] = "This username is already taken. Please try another."
			return render(request, template_name, context)
		except exceptions.ObjectDoesNotExist:
			password1 = register_form.cleaned_data.get("password1")
			password2 = register_form.cleaned_data.get("password2")

			if password1 != password2:
				
				context["error"] = "Passwords don't match. Please try again."
				

			else:
				new_user = User.objects.create(username=username)
				new_user.set_password(password1)
				
				first_name = register_form.cleaned_data.get("first_name")
				last_name  = register_form.cleaned_data.get("last_name")
				email      = register_form.cleaned_data.get("email")

				new_user.first_name = first_name
				new_user.last_name = last_name
				new_user.email = email

				new_user.save()

				return HttpResponseRedirect('/login')

	
	return render(request, template_name, context)


@login_required
def profile_view(request, username):
	context = {}
	template_name = "blogging/profile.html"

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	user = User.objects.get(username=username)

	my_profile = True
	context["whose_profile"] = "My profile"

	current_profile = request.user.profile

	if request.user.username != username:
		my_profile = False
		is_followed = False
		context["whose_profile"] = "Other's Profile"

		
		others_profile = user.profile

		
		if others_profile in current_profile.followed.all():
			is_followed = True

		if not is_followed:
			follow_link = "/follow/" + str(username)
			context["follow_link"] = follow_link
		else:
			follow_link = "Followed !!"
			unfollow_link = "/unfollow/" + str(username)
			context["unfollow_link"] = unfollow_link

		context["is_followed"] = is_followed

		blogs = Blog.objects.filter(author__username=username)
		context["blogs"] = blogs


	followed_people = current_profile.followed.all()
	context["followed_people"] = followed_people


	base_url = "/profile/"
	context["base_url"] = base_url

	context["user"] = user
	context["my_profile"] = my_profile

	if request.user.username == username:
		context["editing"] = {}

		context["editing"]["edit_first_name"] = "edit_first_name"
		context["editing"]["edit_last_name"]  = "edit_last_name"
		context["editing"]["edit_username"]		  = "edit_username"
		context["editing"]["edit_password"]	  = "edit_password"
		context["editing"]["edit_email"]			   = "edit_email"


	blog_form = BlogForm(request.GET or None)
	context["blog_form"] = blog_form

	if blog_form.is_valid():
		title = blog_form.cleaned_data.get("title")
		content = blog_form.cleaned_data.get("content")
		author = User.objects.get(username=username)

		new_blog = Blog.objects.create(title=title, content=content, author=author)

		new_blog.save()

		redirect_url = "/profile/" + str(username) + "/blogs"
		
		return HttpResponseRedirect(redirect_url)


	return render(request, template_name, context)


def show_blogs_view(request, username):
	context = {}
	template_name = "blogging/show_blogs.html"

	blogs = Blog.objects.filter(author__username=username)
	context["blogs"] = blogs

	if request.user.username == username:
		context["same_user"] = True
	else:
		context["same_user"] = False


	return render(request, template_name, context)


def delete_blog_view(request, username, blog_id):
	context = {}
	redirect_url = "/profile/" + str(username) + "/blogs"

	print "I am in delete view"
	Blog.objects.get(id=blog_id).delete()

	return HttpResponseRedirect(redirect_url)


@login_required
def edit_view(request, username, action):
	context = {}
	template_name = "blogging/editing.html"

	if action == "edit_first_name":
		edit_first_name_form = EditFirstNameForm(request.POST or None)
		context['edit_first_name_form'] = edit_first_name_form

		if edit_first_name_form.is_valid():
			new_first_name = edit_first_name_form.cleaned_data.get("new_first_name")
			confirm_new_first_name = edit_first_name_form.cleaned_data.get("confirm_first_name")

			if new_first_name == confirm_new_first_name:

				user = User.objects.get(username=username)
				user.first_name = new_first_name
				user.save()

				redirect_url = "/profile/" + str(request.user.username)
				return HttpResponseRedirect(redirect_url)

			else:
				error = "Input values don't match. Please try again."
				context["error"] = error

	if action == "edit_last_name":
		edit_last_name_form = EditLastNameForm(request.POST or None)
		context["edit_last_name_form"] = edit_last_name_form

		if edit_last_name_form.is_valid():
			new_last_name = edit_last_name_form.cleaned_data.get("new_last_name")
			confirm_new_last_name = edit_last_name_form.cleaned_data.get("confirm_last_name")

			if new_last_name == confirm_new_last_name:

				user = User.objects.get(username=username)
				user.last_name = new_last_name
				user.save()

				redirect_url = "/profile/" + str(request.user.username)
				return HttpResponseRedirect(redirect_url)

			else:
				error = "Input values don't match. Please Try again."
				context["error"] = error

	if action == "edit_username":
		edit_username_form = EditUsernameForm(request.POST or None)
		context["edit_username_form"] = edit_username_form

		if edit_username_form.is_valid():
			new_username = edit_username_form.cleaned_data.get("new_username")
			confirm_new_username = edit_username_form.cleaned_data.get("confirm_new_username")

			if new_username == confirm_new_username:
				try:
					if_any_exists = User.objects.get(username=new_username)

					context["error"] = "This username is already taken. Please try another."
				
				except exceptions.ObjectDoesNotExist:
					user = User.objects.get(username=username)
					user.username = new_username
					user.save()

					redirect_url = "/profile/" + str(new_username)
					return HttpResponseRedirect(redirect_url)

			else:
				error = "Input values don't match. Please Try again."
				context["error"] = error


	if action == "edit_email":
		edit_email_form = EditEmailForm(request.POST or None)
		context["edit_email_form"] = edit_email_form

		if edit_email_form.is_valid():
			new_email = edit_email_form.cleaned_data.get("new_email")
			confirm_new_email = edit_email_form.cleaned_data.get("confirm_new_email")

			if new_email == confirm_new_email:
				user = User.objects.get(username=username)
				user.email = new_email
				user.save()

				redirect_url = "/profile/" + str(request.user.username)
				return HttpResponseRedirect(redirect_url)

			else:
				error = "Input values don't match. Please Try again."
				context["error"] = error

	if action == "edit_password":
		edit_password_form = EditPasswordForm(request.POST or None)
		context["edit_password_form"] = edit_password_form

		if edit_password_form.is_valid():
			new_password = edit_password_form.cleaned_data.get("new_password")
			confirm_new_password = edit_password_form.cleaned_data.get("confirm_new_password")

			if new_password == confirm_new_password:
				user = User.objects.get(username=username)
				user.set_password(new_password)
				user.save()

				redirect_url = "/profile/" + str(request.user.username)
				return HttpResponseRedirect(redirect_url)

			else:
				error = "Input values don't match. Please Try again."
				context["error"] = error


	return render(request, template_name, context)




@login_required
def follow_view(request, username):
	current_profile = request.user.profile
	others_profile = User.objects.get(username=username).profile

	current_profile.followed.add(others_profile)

	redirect_url = "/profile/" + str(username)
	return HttpResponseRedirect(redirect_url)


@login_required
def unfollow_view(request, username):
	current_profile = request.user.profile
	others_profile = User.objects.get(username=username).profile

	current_profile.followed.remove(others_profile)
	redirect_url = "/profile/" + str(username)

	return HttpResponseRedirect(redirect_url)


@login_required
def delete_view(request):
	context = {}
	

	if not request.user.is_authenticated():
		return HttpResponseRedirect("/")

	current_username = request.user.username
	User.objects.get(username=current_username).delete()

	return HttpResponseRedirect("/")


@login_required
def logout_view(request):
	
	logout(request)

	return HttpResponseRedirect("/")
