from django.contrib import admin

from proposition.models import Proposition, Play, Training, Reserve


admin.site.register(Proposition)
admin.site.register(Reserve)
admin.site.register(Play)
admin.site.register(Training)

