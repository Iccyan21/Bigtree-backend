from . import views
from django.urls import path, include

urlpatterns = [
    path('send/',views.SendPostView.as_view()),
    path('getpost/',views.GetPostListView.as_view()),
]
