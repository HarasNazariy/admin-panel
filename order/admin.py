from django.contrib import admin
from .models import Order

@admin.register(Order)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'created_at', 'end_at', 'plated_end_at')
    # list_display = ('id', 'name', 'description', 'get_authors', "year_of_publishing", 'authors', 'issue')

