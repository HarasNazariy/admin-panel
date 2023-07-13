from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from authentication.models import CustomUser
from django.contrib.auth import authenticate, login, logout
from django.db.utils import IntegrityError
from django.views.generic import ListView, DetailView

from django.core.validators import validate_email
from django.core.exceptions import ValidationError, PermissionDenied

from django.contrib.auth.password_validation import validate_password


class IndexView(TemplateView):
    template_name = "authentication/index.html"


def auth_user(request):
    if request.method == 'GET':
        return render(request, "authentication/login.html")
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            email = request.POST["email"]
            password = request.POST["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                error_message = 'Incorrect Login or Password'
                return render(request, template_name='authentication/login.html',
                              context={'error_message': error_message})


def registration(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass']

        # Checking email and password for validation
        try:
            validate_email(email)
            validate_password(password)
        except ValidationError as error_message:
            return render(request, template_name='authentication/registration.html',
                          context={'error_message': error_message})

        # if email and password valid then trying to create the new User
        try:
            user = CustomUser.objects.create_user(email=email, password=password)
            user.save()

        # if email not unique then return 'error_message': 'USER IS ALREADY EXIST'
        except IntegrityError:
            return render(request, template_name='authentication/registration.html',
                          context={'error_message': 'User with that email is already exist, please Log In'})

        # if everything is good then redirect to login page
        return redirect('authentication:login')

    # if request.method != 'POST', just render template
    else:
        return render(request, template_name='authentication/registration.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('index')


class AccountDetails(DetailView):
    model = CustomUser
    template_name = 'authentication/user_account.html'
    context_object_name = 'user_account'

    # Deny to access to another user
    def dispatch(self, request, *args, **kwargs):
        if self.get_object() != request.user:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@login_required
def update_yourself(request, pk):
    if request.method == 'POST' and request.user.id == pk:
        first_name = request.POST['first_name']
        middle_name = request.POST['middle_name']
        last_name = request.POST['last_name']

        try:
            user = CustomUser.get_by_id(pk)
        except CustomUser.DoesNotExist:
            return HttpResponse('User does not exists')

        user.update(first_name=first_name,
                    last_name=last_name,
                    middle_name=middle_name)
        return redirect('authentication:account', pk)


class ListOfUsers(ListView):
    model = CustomUser
    template_name = 'authentication/users.html'
    context_object_name = 'users'
    ordering = 'created_at'

    # Get list without current admin
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.exclude(is_superuser=True).exclude(id=self.request.user.id)


class DetailsOfUser(DetailView):
    model = CustomUser
    template_name = 'authentication/details_user.html'
    context_object_name = 'user'


def update_user(request, pk):
    if request.method == 'POST':

        # check for current_user is admin
        admin = CustomUser.objects.get(id=request.user.id)

        if admin.role == 1 or admin.is_superuser:
            user_to_update = CustomUser.objects.get(id=pk)

            user_to_update.role = int(request.POST['role'])

            if request.POST['active'] == '1':
                user_to_update.is_active = True
            else:
                user_to_update.is_active = False

            user_to_update.save()
            return redirect('authentication:users_list')

    else:
        return redirect('authentication:users_list')
