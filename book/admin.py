from django.contrib import admin
from .models import Book, BookInstance

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_filter = ('id', 'name', 'authors')
    list_display = ('id', 'name', 'description', 'count', 'display_author')
    # list_display = ('id', 'name', 'description', 'get_authors', "year_of_publishing", 'authors', 'issue')

    fieldsets = (
        ('Unchanging Data', {
            'fields': ('name', 'description', 'authors', 'year_of_publishing'),
        }),
        ('Changing Data', {
            'fields': ('count', 'issue'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ('name', 'description', 'authors'),  'year_of_publishing',
        return self.readonly_fields

class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book', 'status', 'due_back',"id")
    

admin.site.register(BookInstance,BookInstanceAdmin)