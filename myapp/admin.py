from django.contrib import admin

# Register your models here.
from .models import user_login, user_details, book_details, user_search

admin.site.register(user_login)
admin.site.register(user_details)
admin.site.register(user_search)
admin.site.register(book_details)

