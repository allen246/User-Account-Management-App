from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm, RecoverPasswordForm, ConfirmPasswordForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

# Create your views here.


def is_student(user):
    return user.is_authenticated and user.role == "student"


def is_staff(user):
    return user.is_authenticated and user.role == "staff"


def is_admin(user):
    return user.is_authenticated and user.role == "admin"


def is_editor(user):
    return user.is_authenticated and user.role == "editor"


class IndexView(View):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


class RegisterView(View):
    template_name = "accounts/register.html"

    def get(self, request):
        form = SignUpForm()
        return render(request, self.template_name, {"form": form, "msg": None})

    def post(self, request):
        form = SignUpForm(request.POST)
        msg = None

        if form.is_valid():
            user = form.save()
            msg = "User created"
            return redirect("login_view")
        else:
            msg = "Form is not valid"

        return render(request, self.template_name, {"form": form, "msg": msg})


class LoginView(View):
    template_name = "accounts/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {"form": form, "msg": None})

    def post(self, request):
        form = LoginForm(request.POST)
        msg = None

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None and user.role and user.role == "admin":
                login(request, user)
                return redirect("adminpage")
            elif user is not None and user.role and user.role == "staff":
                login(request, user)
                return redirect("staff")
            elif user is not None and user.role and user.role == "editor":
                login(request, user)
                return redirect("editor")
            elif user is not None and user.role and user.role == "student":
                login(request, user)
                return redirect("student")
            else:
                msg = "Invalid credentials"
        else:
            msg = "Error validating form"

        return render(request, self.template_name, {"form": form, "msg": msg})


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "password/recovery_password.html"
    form_class = RecoverPasswordForm
    email_template_name = "email/password_reset.html"
    subject_template_name = "email/password_reset_subject.txt"
    success_url = reverse_lazy("index")


class CustomPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    form_class = ConfirmPasswordForm
    template_name = "password/password_reset_confirms.html"
    success_url = reverse_lazy("login_view")


@method_decorator(user_passes_test(is_admin), name="dispatch")
class AdminView(View):
    template_name = "accounts/admin.html"

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(user_passes_test(is_staff), name="dispatch")
class StaffView(View):
    template_name = "accounts/staff.html"

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(user_passes_test(is_student), name="dispatch")
class StudentView(View):
    template_name = "accounts/student.html"

    def get(self, request):
        return render(request, self.template_name)


@method_decorator(user_passes_test(is_editor), name="dispatch")
class EditorView(View):
    template_name = "accounts/editor.html"

    @user_passes_test(is_editor)
    def get(self, request):
        return render(request, self.template_name)
