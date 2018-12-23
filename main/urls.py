from django.urls import path

from . import views
from . import upload_pic
from . import get_pic

urlpatterns = [
    path('', views.index, name='index'),
    path('start', upload_pic.upload_pic, name='upload_pic'),
    path('image', get_pic.get_pic, name='get_pic'),
]
