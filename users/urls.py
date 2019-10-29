from django.urls import path

from .views import SignUpView, UserDetailView, UpdateUserView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('myprofile/', UserDetailView.as_view(), name='profile'),
    path('<int:pk>/edit', UpdateUserView.as_view(), name='edit_profile'),
]
