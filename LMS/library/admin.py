from django.contrib import admin

from .models import Book, Students

# Register your models here.
admin.site.register(Students)
admin.site.register(Book)