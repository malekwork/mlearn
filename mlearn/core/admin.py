from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Post

admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Post)