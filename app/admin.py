from django.contrib import admin
from .models import *

admin.site.register(Question)
admin.site.register(Tag)
admin.site.register(Profile)
admin.site.register(Answer)
admin.site.register(LikeDislike)

# Register your models here.
