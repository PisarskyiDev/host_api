from django.conf.urls.static import static
from django.urls import path

from core import settings
from . import views

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
    path("users/", views.UsersListView.as_view(), name="users-list"),
    path("profile/<int:pk>", views.UsersDetailView.as_view(), name="profile"),
    path("me/", views.SelfUserProfileView.as_view(), name="me"),
    path("shutdown/", views.ShutdownView.as_view(), name="shutdown"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

appname = "host_api"
