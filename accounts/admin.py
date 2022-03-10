from __future__ import unicode_literals, absolute_import
from django.contrib import admin
from django import forms
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin
from .models import User


class MyUserChangeForm(UserChangeForm):
	class Meta(UserChangeForm.Meta):
		model = User

class MyUserCreationForm(UserCreationForm):

	error_message	=	UserCreationForm.error_messages.update({
		'duplicate_username': 'This username has already been taken'
		})

	class Meta(UserCreationForm.Meta):
		model = User

	def clean_username(self):
		username = self.cleaned_data["username"]
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError(self.error_message['duplicate_username'])


class MyUserAdmin(AuthUserAdmin):
	form = MyUserChangeForm
	add_form	=	MyUserCreationForm
	fieldsets = AuthUserAdmin.fieldsets + (
		('Extended Field', {'fields': ('is_HR', 'is_FM', 'is_Manager', 'is_Employee',)}),)

	list_display = ('username', 'first_name', 'last_name', 'is_HR', 'is_FM', 'is_Manager', 'is_Employee', 'is_superuser',)

	list_filter	=	[
		'date_joined',
		'groups',
		'is_superuser',
		'is_staff',
		'is_active',
		]
	readonly_fields	=	[
		'date_joined',
	]

	actions = [
        'activate_users',
        'deactivate_users',
        'staff_users',
        'un_staff_users',
    ]

    
	def activate_users(self, request, queryset):
	    cnt = queryset.filter(is_active=False).update(is_active=True)
	    self.message_user(request, 'Activated {} users.'.format(cnt))
	activate_users.short_description = 'Activate Users'

	def deactivate_users(self, request, queryset):
		cnt = queryset.filter(is_active=True).update(is_active=False)
		self.message_user(request, 'Deactivated {} users.'.format(cnt))
	deactivate_users.short_description = 'Deactivate Users'

	def staff_users(self, request, queryset):
		cnt = queryset.filter(is_staff=False).update(is_staff=True)
		self.message_user(request, 'Staffed {} users.'.format(cnt))
	staff_users.short_description = 'Staff Users'

	def un_staff_users(self, request, queryset):
		cnt = queryset.filter(is_staff=True).update(is_staff=False)
		self.message_user(request, 'Un-staffed {} users.'.format(cnt))
	un_staff_users.short_description = 'Un-staff Users'
 
 
admin.site.register(User, MyUserAdmin)