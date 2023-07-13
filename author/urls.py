from django.urls import path
from author import views
from authentication.urls import access_control


app_name = 'author'

urlpatterns = [
    path("", access_control(views.AuthorPage.as_view()), name='author'),
    path("<int:pk>", access_control(views.AuthorDetails.as_view()), name='details'),

    path("<int:author_id>/remove", access_control(views.remove_author), name='remove_author'),
    path("new/", access_control(views.add_author), name='add_author'),
    path("submit/", access_control(views.submit_add_author), name='submit_new_author')
]
