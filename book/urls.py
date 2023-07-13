from django.urls import path
from book import views
from authentication.urls import access_control
app_name = 'book'


urlpatterns = [
    path("", views.books_page, name='book'),
    path("<int:pk>/", views.BookDetails.as_view(), name='book_details'),
    path("addbook", access_control(views.add_book_view), name='add_book'),
    path("<int:book_id>/remove", access_control(views.remove_book), name='remove_book'),
]
