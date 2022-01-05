from django.urls import path

from . import views

app_name = 'bi'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('api/predict/', views.UserPredictAPIView.as_view(), name="predict_User_api"),
    path('chart', views.ChartView.as_view(), name="chart"),
]