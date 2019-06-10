from .views import views
from django.conf.urls import url


app_name = 'pkchanger'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(
        template_name='pkchanger/index.html'), name='index'),
]
