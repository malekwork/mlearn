from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Category, Post, Comment

admin.site.register(Category, DraggableMPTTAdmin)
admin.site.register(Post)
admin.site.register(Comment)