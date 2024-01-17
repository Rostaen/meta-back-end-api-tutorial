from django.contrib import admin
from .models import BookItem, Category

# Register your models here.
admin.site.register(BookItem)
admin.site.register(Category)
