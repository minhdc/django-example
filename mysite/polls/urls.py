from django.urls import path
from . import views

app_name = 'polls'
#urlpatterns = [
#    path('',views.index,name='index'),
#    path('<int:question_id>',views.detail,name='detail'),
#    path('<int:question_id>/results/',views.results,name='results'),
#    path('<int:question_id>/vote/',views.vote,name='vote'),
#    path('specifics/<int:question_id>/',views.detail,name='detail'),
#]
urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('<int:pk>/',views.DetailView.as_view(),name='detail'),
    path('<int:pk>/result/',views.ResultsView.as_view(),name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
]
