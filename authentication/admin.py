from django.contrib import admin
from .models import CustomUser



@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'middle_name', 'email','created_at','updated_at','is_active')
    # list_display = ('id', 'name', 'description', 'get_authors', "year_of_publishing", 'authors', 'issue')

