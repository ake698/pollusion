from django.contrib import admin
from app.models import *
from django.contrib.auth.admin import User,Group
# Register your models here.
class UMAdmin(admin.ModelAdmin):
    list_display = ('id','username','password')

class UMData(admin.ModelAdmin):
    list_display = ("id",'date','qualityLevel','AQI','PM25','PM10','SO2','NO2','CO','O3')
    list_per_page = 50

admin.site.register(UserManager,UMAdmin)
admin.site.register(Airquality,UMData)
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.site_header = "后台管理"
admin.site.site_title = "后台管理"