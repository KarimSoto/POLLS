from django.urls import path

from . import views



app_name = "polls"
urlpatterns = [
    path("polls/", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("<int:pk>/results/", views.results, name="results"),
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path('', views.Index, name="superindex"),
    path('mv1/', views.my_view1, name='my_view1'),
    path('mv2/', views.my_view2, name='my_view2'),
    
]