from django.urls import path

from . import views

app_name = "bbs"
urlpatterns = [
    # path('', views.index, name='index'),
    path('', views.QuestionListView.as_view(), name='index'),
    path('my-page', views.my_page, name='my-page'),
    # ex: /bbs/5/
    # path('<int:question_id>/', views.detail, name='detail'),
    path('<int:question_id>/', views.DetailListView.as_view(), name='detail'),
    # ex: /bbs/5/reply/
    path('<int:question_id>/reply/', views.reply, name='reply'),
    # ex: /bbs/topic/
    # path('topic/', views.topic, name="topic"),
    path('topic/', views.TopicCreateView.as_view(), name="topic"),
    path('topic-update/', views.TopicUpdateView.as_view(), name="topic-update"),
]