from django.contrib import admin
from .models import Entry,UserDetail,RatingHistory
# Register your models here.

admin.site.register(Entry)
admin.site.register(UserDetail)
admin.site.register(RatingHistory)
