from django.urls import path
from order import views

app_name = 'order'


urlpatterns = [
    path('', views.order_view, name='order_view'),
    path('close/', views.close_order, name='close_order'),
    path('user/', views.show_books_for_user, name='book_for_user'),
]
