from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Team

class AccountAdmin(UserAdmin):
	list_display = ('email','date_joined','username','first_name','last_name','is_captain', 'team', 'numTel',)
	search_fields = ('email','username', 'team')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal= ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account,AccountAdmin)
admin.site.register(Team)
