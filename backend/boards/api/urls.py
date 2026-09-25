from django.urls import path
from .views import BoardListView, BoardDetailView, EmailCheckView, TaskCreateView


urlpatterns = [
    path('boards/', BoardListView.as_view(), name="boards-list"),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name="boards-detail"),
    path('email-check/', EmailCheckView.as_view(), name="email-check"),
    path('tasks/', TaskCreateView.as_view(), name="new-task")
    # path('login/', LoginView.as_view(), name="login")
]
