from django.contrib import admin
from accounts.models import AccessToken,User,UserFollow,UserBlock

admin.site.register(AccessToken)
admin.site.register(User)
admin.site.register(UserFollow)
admin.site.register(UserBlock)
 
# Register your models here.
