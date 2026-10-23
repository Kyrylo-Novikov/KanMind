from django.urls import path
from .views import BoardListView, BoardDetailView, EmailCheckView, TaskCreateView, TaskUpdateView, CommentListView, CommentDetailView, AssignedToMeView, ReviewingView


urlpatterns = [
    path('boards/', BoardListView.as_view(), name="boards-list"),
    path('boards/<int:pk>/', BoardDetailView.as_view(), name="boards-detail"),
    path('email-check/', EmailCheckView.as_view(), name="email-check"),
    path('tasks/', TaskCreateView.as_view(), name="new-task"),
    path('tasks/<int:pk>/', TaskUpdateView.as_view(), name="task-detail"),
    path('tasks/<int:pk>/comments/',
         CommentListView.as_view(), name="comment-list"),
    path('tasks/<int:pk>/comments/<int:comment_pk>/',
         CommentDetailView.as_view(), name="comment-detail"),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view(), name='assigned-to-me'),
    path('tasks/reviewing/', ReviewingView.as_view(), name='reviewer')
]
