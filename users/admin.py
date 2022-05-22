from django.contrib import admin
from users.models import *

# Register your models here.

class ProfileAdmin(admin.ModelAdmin):
    pass
class FollowAdmin(admin.ModelAdmin):
    pass


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Follow, FollowAdmin)