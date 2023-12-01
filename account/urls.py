from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("login/", views.LoginView.as_view(), name="login_view"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("password-reset/", views.ResetPasswordView.as_view(), name="password_reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("logout/", auth_views.LogoutView.as_view(next_page="index"), name="logout"),
    path("adminpage/", views.AdminView.as_view(), name="adminpage"),
    path("staff/", views.StaffView.as_view(), name="staff"),
    path("student/", views.StudentView.as_view(), name="student"),
    path("editor/", views.EditorView.as_view(), name="editor"),
]
