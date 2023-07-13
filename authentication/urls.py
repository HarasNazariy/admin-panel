from django.contrib.auth import logout
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

from authentication import views
from django.urls import path

app_name = 'authentication'


# check role and authenticated. Access to urls only for authenticated user with role = 1 (admin)
def access_control(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('authentication:login')
        elif request.user.role == 1:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("403 Forbidden")
    return wrapper


urlpatterns = [
    path("registration/", views.registration, name='registration'),
    path("login/", views.auth_user, name='login'),
    path("logout/", views.logout_view, name='logout'),

    path("account/<int:pk>", views.AccountDetails.as_view(), name="account"),
    path("account/update/<int:pk>", views.update_yourself, name="update_yourself"),

    path("users/", access_control(views.ListOfUsers.as_view()), name="users_list"),
    path("users/<int:pk>", access_control(views.DetailsOfUser.as_view()), name="users_details"),
    path("users/<int:pk>/update", access_control(views.update_user), name='update_user')
]
