from django.contrib import admin
from .models import Blog, Photo, Comment
# Register your models here.

#photo 클래스를 inline으로 나타낸다.
class PhotoInline(admin.TabularInline):
    model = Photo

# Post 클래스는 해당하는 Photo 객체를 리스트로 관리한다.
class PostAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]

admin.site.register(Blog, PostAdmin)
admin.site.register(Comment)
