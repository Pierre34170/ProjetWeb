from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import Account, Team, BelongToTeam

class AccountAdmin(UserAdmin):
	list_display = ('email','date_joined','username','first_name','last_name','is_captain', 'numTel',)
	search_fields = ('email','username')
	readonly_fields = ('date_joined', 'last_login')

	filter_horizontal= ()
	list_filter = ()
	fieldsets = ()

admin.site.register(Account,AccountAdmin)
admin.site.register(Team)
admin.site.register(BelongToTeam)
