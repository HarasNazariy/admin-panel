from django.contrib import admin
from .models import Author

#admin.site.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'surname', 'patronymic', 'id')


# Register the admin class with the associated model
admin.site.register(Author, AuthorAdmin)
